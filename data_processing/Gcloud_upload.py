# Script for uploading tfrecords and model checkpoints, model configs to gcloud + learning initialisation
import os

project_dir = os.getcwd()
train_dir = os.path.join(project_dir, 'data/train.record')
eval_dir = os.path.join(project_dir, 'data/eval.record')
label_dir = os.path.join(project_dir, 'Starthack/configs_labels/label_map.pbtxt')

models = ['faster_rcnn_resnet']
for model in models:
	model_dir = os.path.join(project_dir, 'Models/' + model)
	config_dir = os.path.join(project_dir, 'Starthack/model_configs/' + 'pipeline' + '.config')
	# load necessary data into glouc
	os.system("gsutil cp " + train_dir + " gs://starthack/data_" + model + "/train.record")
	os.system("gsutil cp " + eval_dir +  " gs://starthack/data_" + model + "/eval.record")
	os.system("gsutil cp " + label_dir + " gs://starthack/data_" + model + "/label_map.pbtxt")
	os.system("gsutil cp " + model_dir + "/model.ckpt.* gs://starthack/data_"+ model + "/")
	os.system("gsutil cp " + config_dir + " gs://starthack/data_" + model + "/pipeline.config")

	# cloud storage
	gs_storage = "gs://starthack/data_" + model
	gs_model = "gs://starthack/model_dir_" + model
	# object detection API paths
	tf_api_path = "D:\\object_detection_api\\models\\research"
	cluster_config_p = os.path.join(project_dir, "Starthack\configs_labels\cloud_config_single.yml")
	# submit training job (from research

	console_cmd = "gcloud ml-engine jobs submit training "
	job_name = "cw_train_3" + model
	runtime = " --runtime-version 1.9"
	job_dir = " --job-dir=" + gs_storage
	packages = " --packages " + os.path.join(tf_api_path, "dist/object_detection-0.1.tar.gz")+ "," + os.path.join(tf_api_path, "slim/dist/slim-0.1.tar.gz") + "," + os.path.join(tf_api_path, "pycocotools-2.0.tar.gz")
	module = " --module-name " +  os.path.join(tf_api_path, "object_detection.model_main")
	region = " --region us-central1"
	cluster_config = " --config " + cluster_config_p
	model_dir = " -- --model_dir=" + gs_model
	pipeline_config = " --pipeline_config_path=" + gs_storage + "pipeline.config"
	project_id = " --project=" + "starthack"

	ml_engine = console_cmd + job_name + runtime + job_dir + packages + module + region	 + cluster_config + model_dir + pipeline_config + project_id

	os.system(ml_engine)



# funktionierender code
#(base) C:\Users\thoma\tensorflow\models\research> gcloud ml-engine jobs submit training logodetec_v1 --runtime-version 1.9 --job-dir=gs://logo_detection_v1/model_dir --packages dist/object_detection-0.1.tar.gz,slim/dist/slim-0.1.tar.gz,pycocotools-2.0.tar.gz --module-name object_detection.model_main --region us-central1 --config object_detection/samples/cloud/cloud.yml -- --model_dir=gs://logo_detection_v1/model_dir --pipeline_config_path=gs://logo_detection_v1/data_1/pipeline.config
#Job [logodetec_v1] submitted successfully.
#Your job is still active. You may view the status of your job with the command
#
#  $ gcloud ml-engine jobs describe logodetec_v1
#
#or continue streaming the logs with the command
#
#  $ gcloud ml-engine jobs stream-logs logodetec_v1
#jobId: logodetec_v1
#state: QUEUED