import os
import chardet

class SRTConverter:
    def __init__(self, input_folder, output_folder=None):
        self.folder = input_folder
        self.output_folder = output_folder

    def detect_encoding(self, file_path):
        import chardet
        with open(file_path, "rb") as f:
            result = chardet.detect(f.read())
        return result["encoding"]

    def convert_all(self, output_format="vtt"):
        converted = 0
        for file in os.listdir(self.folder):
            if file.endswith(".srt"):
                path_srt = os.path.join(self.folder, file)
                output_file = file.replace(".srt", f".{output_format}")
                output_path = os.path.join(self.output_folder or self.folder, output_file)

                encoding = self.detect_encoding(path_srt)

                with open(path_srt, "r", encoding=encoding) as f_srt:
                    lines = f_srt.readlines()

                with open(output_path, "w", encoding="utf-8") as f_out:
                    if output_format == "vtt":
                        f_out.write("WEBVTT\n\n")
                        for line in lines:
                            f_out.write(line.replace(",", "."))

                    elif output_format == "txt":
                        for line in lines:
                            if not line.strip().isdigit() and "-->" not in line:
                                f_out.write(line)

                    elif output_format == "csv":
                        f_out.write("Number,Time,Text\n")
                        num, time, text = "", "", ""
                        for line in lines:
                            if line.strip().isdigit():
                                num = line.strip()
                            elif "-->" in line:
                                time = line.strip().replace(",", ".")
                            elif line.strip():
                                text = line.strip()
                                f_out.write(f'"{num}","{time}","{text}"\n')

                converted += 1
        return converted