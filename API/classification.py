import requests
from io import BytesIO
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from matplotlib import pyplot as plt
from PIL import Image
from object_detection.utils import ops as utils_ops
import os
import PIL

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def getURL(x, y):
	return 'http://maps.google.com/maps/api/staticmap?center=' + str(y) + ',' + str(x) + '&zoom=19&size=500x500&scale=2&maptype=satellite&key=[YOUR_API_KEY]'

def saveSquare(x,y):
			response =requests.get(getURL(x,y))
			img = Image.open(BytesIO(response.content))
			img = img.resize((1000,1000), PIL.Image.ANTIALIAS)
			imgName = str(x).replace('.','') + str(y).replace('.','') + '.png'
			if os.path.isfile(imgName):
				os.remove(imgName)
			img.save(imgName)
			return(imgName)



def loadModel():
	detection_graph = tf.Graph()
	with detection_graph.as_default():
		od_graph_def = tf.GraphDef()
		with tf.gfile.GFile("Starthack/inference_graph/frozen_inference_graph.pb", 'rb') as fid:
			serialized_graph = fid.read()
			od_graph_def.ParseFromString(serialized_graph)
			tf.import_graph_def(od_graph_def, name='')
	return(detection_graph)

detection_graph = loadModel()

def run_inference_for_single_image(image, graph):
  with graph.as_default():
    with tf.Session() as sess:
      # Get handles to input and output tensors
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks'
      ]:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
              tensor_name)
      if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

      # Run inference
      output_dict = sess.run(tensor_dict,
                             feed_dict={image_tensor: np.expand_dims(image, 0)})

      # all outputs are float32 numpy arrays, so convert types as appropriate
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
  return output_dict


def box_extractor(boxes, scores, img_width, img_height):
	# ymin,xmin,ymax, xmax
	boxes_relevant = []
	box_centers = []
	for box, score in zip(boxes, scores):
		if score > 0.5:
			boxes_relevant.append(box)
			x_mean = (box[1] + box[3])/2
			y_mean = (box[0] + box[2])/2
			box_centers.append([x_mean * img_width, y_mean * img_height])
	return(box_centers)


def cwClassification(x,y, inference_graph):
	imgName = saveSquare(x,y)
	IMAGE_SIZE = (8, 8)
	PATH_TO_LABELS = "Starthack/configs_labels/label_map.pbtxt"
	NUM_CLASSES = 1

	label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
	categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
	category_index = label_map_util.create_category_index(categories)

	image = Image.open(imgName)
	width = image.width
	height = image.height
	center_img = [width/2, height/2]
	image = image.convert('RGB')
	image.save('test.jpg')
	img_np = load_image_into_numpy_array(image)
	output_dict = run_inference_for_single_image(img_np, inference_graph)

	vis_util.visualize_boxes_and_labels_on_image_array(
		img_np,
		output_dict['detection_boxes'],
		output_dict['detection_classes'],
		output_dict['detection_scores'],
		category_index,
		instance_masks=output_dict.get('detection_masks'),
		use_normalized_coordinates=True,
		line_thickness=6)
	plt.figure(figsize=IMAGE_SIZE)
	plt.imshow(img_np)
	outFile = 'Starthack/API/detection_boxes.png'
	if os.path.isfile(outFile):
		os.remove(outFile)
	plt.savefig(outFile)

	centers = box_extractor(output_dict['detection_boxes'], output_dict['detection_scores'], width, height)
	def getClosestCW(points):
		dist_min = 100000000
		for point in points:
			dist = ((point[0] - center_img[0])**2 + (point[1] - center_img[1])**2)**0.5
			if(dist_min > dist):
				dist_min = dist
				point_min = point
		return(point_min)
	closestCW = getClosestCW(centers)

	geo_codConsy = 0.000005614 * 0.175
	geo_codConsx = 0.000005614 * 0.2325
	x_dist = (closestCW[0] - center_img[0]) * geo_codConsx
	y_dist = -(closestCW[1] - center_img[1]) * geo_codConsy

	cw_geoCodx = x + x_dist
	cw_geoCody = y + y_dist
	return(cw_geoCodx, cw_geoCody)



x = 7.4296
y= 46.9432

xy = cwClassification(x,y, detection_graph)


