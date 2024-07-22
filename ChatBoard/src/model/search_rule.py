import os

def search_rule(game_name : str) -> str:
    current_directory = os.getcwd()
    search_folder = os.path.join(current_directory, 'data')
    files_in_folder = os.listdir(search_folder)

    # game_name과 동일한 이름의 PDF 파일 찾기 - 영어로 띄어쓰기 없이 입력
    target_file_name = f"{game_name}.pdf"

    if target_file_name in files_in_folder:
        return os.path.join(search_folder, target_file_name)
    else:
        return None  # 파일이 없을 경우 None 반환)


if __name__ == "__main__":
  print(search_rule("halligalli"))
