import requests

URL = "http://localhost:8000/extract"
FILE_PATH = "sample.docx"


def test_extractor():
    with open(FILE_PATH, "rb") as f:
        files = {
            "file": (FILE_PATH, f, "application/pdf")
        }

        response = requests.post(URL, files=files)

    print("Status:", response.status_code)

    if response.status_code == 200:
        data = response.json()
        print("Filename:", data["filename"])
        print("\nExtracted text preview:\n")
        print(data["text"])
    else:
        print(response.text)


if __name__ == "__main__":
    test_extractor()