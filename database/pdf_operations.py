from database_operation import *
import fitz

def extract_images(input_file_path, output_dir_path, paper_index):
    pdf_split = os.path.split(input_file_path)
    pdf_name = pdf_split[-1]
    _pdf_split = os.path.splitext(pdf_name)
    pdf_name_without_ext = _pdf_split[0]

    file = fitz.open(input_file_path)

    img_count = 0
    len_xref = file.xref_length()

    print(f"[PDF_INFO] filename:{pdf_name}, pages: {len(file)}, object: {len_xref - 1}")

    for page in file:
        try:
            tuple_image = page.get_images()
            lst_image = list(tuple_image)
            for xref_tuple in lst_image:
                xref = list(xref_tuple)[0]
                print(f"[IMG_INFO]paperIndex: {paper_index} imgID: {img_count} xref: {xref}")
                img = file.extract_image(xref)
                image_filename = f"{img_count}." + img["ext"]
                image_filename = os.path.join(output_dir_path, image_filename)
                print(f"[OUTPUT_INFO]{image_filename}")
                img_out = open(image_filename, 'wb')
                img_out.write(img["image"])
                img_out.close()
                img_count += 1
        except Exception as e:
            print(e)


if __name__ == '__main__':
    ### test
    # input_file_path = '/mnt/e/2023fall/ICE2604/database/100_PDF/elsevier_0d8e1fc979302d36e57072865329cbb30781292d.pdf'
    # output_file_path = '/mnt/e/2023fall/ICE2604/database/100_PDF_pics/test'
    # extract_images(input_file_path, output_file_path, paper_index=1)

    input_dir_path = '/mnt/e/2023fall/ICE2604/database/100_PDF'
    output_dir_path = '/mnt/e/2023fall/ICE2604/database/100_PDF_pics'
    for root, dirs, files in os.walk(input_dir_path):
        print(f"root: {root}")
        print(f"dirs: {dirs}")
        print(f"files: {files}")
        for i, file in enumerate(files):
            # print(file[:-4])
            try:
                img_dir = file[:-4]
                if not os.path.exists(os.path.join(output_dir_path, img_dir)):
                    os.makedirs(os.path.join(output_dir_path, img_dir))
                else:
                    continue
                input_file_path = os.path.join(input_dir_path, file)
                extract_images(input_file_path, os.path.join(output_dir_path, img_dir), i)
            except Exception as e:
                print(f"[ERROR]{file}:{e}")