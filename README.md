# pompeii_explorer

Manual inspection with web interface

```usage: server.py [-h]
                 image_folder raw_image_folder marked_page_folder
                 alignment_csv ocr_text load_previous_state

Web interface to mark incorrect extractions

positional arguments:
  image_folder         Path where pictures have been auto-extracted
  raw_image_folder     Path of PDF page images
  marked_page_folder   Path where incorrect pages will be stored
  alignment_csv        Path of csv where image and text is aligned
  ocr_text             Path of text file where OCR text is stored
  load_previous_state  Load previously saved progress

optional arguments:
  -h, --help           show this help message and exit
  ```
  
Eg. python server.py ../final_extraction/PPMM ../page_images/PPM4 ../final_extraction/trial4 ../final_extraction/PPM4-aligned.csv ../PPM/PPM_text_files/PPM_4ocr.txt False
