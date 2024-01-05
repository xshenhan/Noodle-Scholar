import os
import pdfplumber
import camelot
from pdf2image import convert_from_path
import torch
import numpy as np
from tqdm import tqdm

from detectron2.config import get_cfg
from detectron2.engine.defaults import DefaultPredictor

import warnings

warnings.filterwarnings("ignore")


class TableDetector(object):
    def __init__(self, yaml_path, weight_path):
        cfg = get_cfg()
        cfg.merge_from_file(yaml_path)
        cfg.merge_from_list(["MODEL.WEIGHTS", weight_path])
        cfg.MODEL.RETINANET.SCORE_THRESH_TEST = 0.9
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.9
        cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = 0.9
        cfg.MODEL.DEVICE = "cuda:0"
        cfg.freeze()
        self.predictor = DefaultPredictor(cfg)

    def predict_image(self, image_array):
        predictions = self.predictor(image_array)
        height, width = predictions["instances"].to(torch.device("cpu")).image_size
        height, width = int(height), int(width)
        res_boxes = predictions["instances"].to(torch.device("cpu")).get_fields()['pred_boxes'].tensor.numpy().tolist()
        areas = []
        for box in res_boxes:
            areas.append([int(box[0]) / width, int(box[1]) / height, int(box[2]) / width, int(box[3]) / height])
        return areas

    def predict_file(self, pdf_file_path):
        all_page_areas = []
        page_images = convert_from_path(pdf_file_path)
        for page_image in page_images:
            page_image = np.array(page_image)
            try:
                current_page_areas = self.predict_image(page_image)
            except RuntimeError:
                current_page_areas = []
            all_page_areas.append(current_page_areas)
        return all_page_areas


def get_pdf_h_and_w(pdf_path):
    all_page_h_and_w = []
    with pdfplumber.open(pdf_path) as f:
        for current_page in f.pages:
            all_page_h_and_w.append([current_page.height, current_page.width])
    return all_page_h_and_w


def main():
    input_dir = "100_pdfs"
    output_dir = "100_pdfs_output"
    yaml_path = "model/All_X152.yaml"
    weight_path = "model/model_final.pth"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    input_pdf_names = os.listdir(input_dir)

    table_detector = TableDetector(yaml_path=yaml_path, weight_path=weight_path)
    for input_pdf_name in tqdm(input_pdf_names):
        input_pdf_path = os.path.join(input_dir, input_pdf_name)
        output_table_dir = os.path.join(output_dir, ".".join(input_pdf_name.split(".")[:-1]))
        if not os.path.exists(output_table_dir):
            os.mkdir(output_table_dir)
        all_page_areas = table_detector.predict_file(input_pdf_path)
        all_page_h_and_w = get_pdf_h_and_w(input_pdf_path)
        for page_id, page_areas in enumerate(all_page_areas):
            if len(page_areas) == 0:
                continue
            h, w = all_page_h_and_w[page_id]
            current_tables_boxes = [str([pa[0] * w, (1 - pa[1]) * h, pa[2] * w, (1 - pa[3]) * h]).replace(" ", "")[1: -1] for pa in page_areas]
            # print(current_tables_boxes)
            try:
                current_tables = camelot.read_pdf(
                    input_pdf_path, pages=str(page_id+1), flavor="stream", table_areas=current_tables_boxes
                )
            except (ValueError, IndexError):
                continue
            current_tables.export(os.path.join(output_table_dir, 'output.csv'), f='csv', compress=False)


if __name__ == '__main__':
    main()
