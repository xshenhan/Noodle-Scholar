import zipfile
import os
import shutil

def extract_and_organize(zip_folder_path):
    # Ensure the zip_folder_path is an absolute path
    zip_folder_path = os.path.abspath(zip_folder_path)

    # Create main output directories
    text_output_dir = os.path.join(zip_folder_path, '100_PDF_text')
    csv_main_dir = os.path.join(zip_folder_path, '100_PDF_csv')
    png_main_dir = os.path.join(zip_folder_path, '100_PDF_table_rendition')

    # Check if they exist, if not create them
    for dir_path in [text_output_dir, csv_main_dir, png_main_dir]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    # Sort files by their numerical identifier
    def sort_files(filename):
        base_name = os.path.splitext(filename)[0]
        identifier = int(base_name.split("part")[-1])
        return identifier

    # Iterate through each zip file in the specified directory
    for zip_file in os.listdir(zip_folder_path):
        if zip_file.endswith('.pdf.zip'):
            file_name = zip_file.split('.pdf.zip')[0]
            print(f'Extracting {file_name}...')

            # Create individual directories for each file_name inside csv_main_dir and png_main_dir
            file_csv_dir = os.path.join(csv_main_dir, file_name)
            file_png_dir = os.path.join(png_main_dir, file_name)
            os.makedirs(file_csv_dir, exist_ok=True)
            os.makedirs(file_png_dir, exist_ok=True)

            # Extract the zip file
            with zipfile.ZipFile(os.path.join(zip_folder_path, zip_file), 'r') as zip_ref:
                temp_extract_path = os.path.join(zip_folder_path, f'temp_{file_name}')
                zip_ref.extractall(temp_extract_path)

                # Move json to the 100PDF_text folder
                json_file_path = os.path.join(temp_extract_path, 'structuredData.json')
                if os.path.exists(json_file_path):
                    shutil.move(json_file_path, os.path.join(text_output_dir, f'{file_name}.json'))

                # Handle png and csv files
                inner_folder = os.path.join(temp_extract_path, "tables")
                if os.path.exists(inner_folder):
                    csv_count = 0
                    png_count = 0

                    sorted_files = sorted(os.listdir(inner_folder), key=sort_files)
                    for inner_file in sorted_files:
                        if inner_file.endswith('.csv'):
                            new_name = f"{csv_count}.csv"
                            shutil.move(
                                os.path.join(inner_folder, inner_file),
                                os.path.join(file_csv_dir, new_name)
                            )
                            csv_count += 1
                        elif inner_file.endswith('.png'):
                            new_name = f"{png_count}.png"
                            shutil.move(
                                os.path.join(inner_folder, inner_file),
                                os.path.join(file_png_dir, new_name)
                            )
                            png_count += 1

                # Remove temporary folder
                shutil.rmtree(temp_extract_path)

if __name__ == "__main__":
    # Provide the path to your directory containing zip files here
    directory_path = "C:/Users/huanyu/Desktop/pdfservices-python-sdk-samples-main/output"
    extract_and_organize(directory_path)