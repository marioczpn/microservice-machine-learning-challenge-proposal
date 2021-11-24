import os
import requests

class TestBasic():

    API_ENDPOINT_PROCESS='http://localhost:80/api/face-detection'

    def test_apiproducerms_up_running(self):
            response = requests.get(url='http://localhost:80/health')
            assert response.status_code == 200

    def test_process_send_one_image_status_code_equals_200(self):
            main_script_dir = os.path.dirname(__file__)
            rel_path = "fixtures/images/Aaron_Eckhart_0001.jpg"
            image_file = os.path.join(main_script_dir, rel_path)
            payload = {"image_files": open(image_file, "rb")}
            response = requests.post(url=self.API_ENDPOINT_PROCESS, files=payload)
           
            print(f"Request: {payload}")
            print(f"Response:{response.json()}")
            assert ['["Aaron_Eckhart_0001.jpg", [[67, 66, 118, 118]]]'] == response.json()
            assert response.status_code == 200

    def test_send_multiple_images_status_code_equals_200(self):
            main_script_dir = os.path.dirname(__file__)
            rel1 = "fixtures/images/Aaron_Eckhart_0001.jpg"
            first_image = os.path.join(main_script_dir, rel1)

            rel2 = "fixtures/images/Ahmed_Lopez_0001.jpg"
            second_image = os.path.join(main_script_dir, rel2)

            rel3 = "fixtures/images/Alan_Mulally_0001.jpg"
            third_image = os.path.join(main_script_dir, rel3)

            rel4 = "fixtures/images/Alex_Corretja_0001.jpg"
            fourth_image = os.path.join(main_script_dir, rel4)
            
            rel5 = "fixtures/images/Anne_Donovan_0001.jpg"
            fifth_image = os.path.join(main_script_dir, rel5)
            
            payload = [
                ('image_files', open(first_image, "rb")), ('image_files', open(second_image, "rb")), ('image_files', open(third_image, "rb")), 
                ('image_files', open(fourth_image, "rb")), ('image_files', open(fifth_image, "rb"))]
            response = requests.post(url=self.API_ENDPOINT_PROCESS, files=payload)

            expected_result = ['["Aaron_Eckhart_0001.jpg", [[67, 66, 118, 118]]]', 
                               '["Ahmed_Lopez_0001.jpg", [[65, 65, 122, 122]]]', 
                               '["Alan_Mulally_0001.jpg", [[63, 63, 123, 123]]]', 
                               '["Alex_Corretja_0001.jpg", [[71, 67, 114, 114]]]', 
                               '["Anne_Donovan_0001.jpg", [[64, 68, 118, 118]]]']
            
            print(f"Request: {payload}")
            print(f"Response:{response.json()}")
            assert expected_result == response.json()
            assert response.status_code == 200
