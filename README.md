# Starthack

[Roadmap](https://docs.google.com/spreadsheets/d/1ABSrxaIwR5E6rwZBSUIWMA2xzvysyv4jfu43l3_eTzM/edit?usp=sharing)

## TF Transfer-learning setup

*(1)* Install tensorflow object detection API (see pdf)

*(2)* Create xml labels with [LABELIMG](https://github.com/tzutalin/labelImg)

*(3)* Split data into training and evaluation directory

*(4)* Create TFR-Files (Tensorflow readable files)

*(5)* Download model checkpoints from here [MODELZOO](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)

*(6)* Customize model configuraitons (see model_configs)

*(7)* Setup GCloud Account + Projekt [Documentation](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/running_pets.md)

*(8)* Load config+ training data + eval_data + labelmap + model checkpoint into Gcloud Storage

*(9)* Start ML-Engine Job


from PIL import Image

im = Image.open("Ba_b_do8mag_c6_big.png")
rgb_im = im.convert('RGB')
rgb_im.save('colors.jpg')
