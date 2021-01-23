import detect
import group_object as go
import generate_description_for_images as gen
json_directory = 'json'


detect.detect()
go.group_all_files(json_directory)
gen.generate(json_directory)
