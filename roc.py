import numpy as np
import h5py
import os
import matplotlib.pyplot as plt
import shutil
import sys
import argparse

sys.path.append('/usr/local/lib/python2.7/dist-packages')
import cv2

prob_thres = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.15, 0.20, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8,
			  0.9, 0.92, 0.94, 0.95, 0.96, 0.97,
			  0.971, 0.972, 0.973, 0.974, 0.975, 0.976, 0.977, 0.978, 0.979, 0.98,
			  0.981, 0.982, 0.983, 0.984, 0.985, 0.986, 0.987, 0.988, 0.989,
			  0.99, 0.991, 0.992, 0.993, 0.994, 0.995, 0.996, 0.997, 0.998, 0.999, 0.9999, 0.99999]


def iou(b1, b2):
	iou_val = 0.0
	x1 = np.max([b1[0], b2[0]])
	y1 = np.max([b1[1], b2[1]])
	x2 = np.min([b1[0] + b1[2], b2[0] + b2[2]])
	y2 = np.min([b1[1] + b1[3], b2[1] + b2[3]])
	w = np.max([0, x2 - x1])
	h = np.max([0, y2 - y1])
	if w != 0 and h != 0:
		iou_val = float(w * h) / (b1[2] * b1[3] + b2[2] * b2[3] - w * h)
	return iou_val


def recall(pred, gt, thres):
	n = len(gt)
	if len(gt) == 0:
		reca = 1.0
		return reca
	if len(pred) == 0:
		reca = 0.0
		return reca

	m = 0
	for b1 in gt:
		for b2 in pred:
			if iou(b1, b2) > thres:
				m += 1
				break
	reca = float(m) / n
	return reca


def precision(pred, gt, thres):
	n = len(pred)
	if len(pred) == 0:
		prec = 1.0
		return prec
	if len(gt) == 0:
		prec = 1.0 / (len(pred) + 1)
		return prec
	m = 0
	for b1 in pred:
		for b2 in gt:
			if iou(b1, b2) > thres:
				m += 1
				break
	prec = float(m) / n
	return prec


def get_gt(file_path, anno_key, resized_height, scale_range):
	print(file_path)
	with h5py.File(file_path, 'r') as f:
		if anno_key in f.keys():
			gt = f[anno_key][:]
			if len(gt) == 0 or gt.size == 0:
				return []
			assert "img_info" in f.keys(), "h5 file doesnt have img_info key"
			height, width = f["img_info"][:]
			scale_range_resized = height * 1.0 / resized_height * np.array(scale_range)
			inds = np.where((gt[:, 2] >= scale_range_resized[0]) & (gt[:, 2] < scale_range_resized[1]))[0]
			gt = gt[inds, :]
		else:
			gt = []
	return gt


def get_pred_txt(file_path, is_include_cls, scale_range):
	probs = []
	bbs = []
	print file_path
	with open(file_path, 'r') as f:
		
		try:
			while True:
				line = f.next().strip()
				lst = line.split()
				print line, lst
				if is_include_cls:
					pred = map(int, lst[1:5])
					score = float(lst[5])
				else:
					pred = map(int, lst[:4])
					score = float(lst[4])
				if pred[2] >= scale_range[0] and pred[2] < scale_range[1]:
					bbs.append(pred)
					probs.append(score)
		except StopIteration:
			pass

	return np.array(bbs), np.array(probs)


def show(img_path, gt, pred, prob, thres=0.3):
	img = cv2.imread(img_path)

	for bbox in gt:
		cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2] - 1, bbox[1] + bbox[3] - 1), (0, 0, 255), 2)
	# cv2.putText(img, str(bbox[0])+" "+str(bbox[1]), (bbox[0],bbox[1]+bbox[3]-1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0,255), 1)

	I = prob > thres
	prob_k = prob[I]
	pred_k = pred[I, :]
	for bbox, pb in zip(pred_k, prob_k):
		cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2] - 1, bbox[1] + bbox[3] - 1), (0, 255, 0), 2)
		cv2.putText(img, str(pb), (bbox[0], bbox[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
	# cv2.putText(img, str(bbox[0])+" "+str(bbox[1]), (bbox[0],int(bbox[1]+bbox[3]/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
	cv2.imshow("test", img)
	cv2.waitKey(0)


def roc(gt_pred_file, save_dir, anno_key, iou_thres, is_include_cls, resized_height, scale_range):
	lines = open(gt_pred_file, 'r').readlines()
	precisions = list()
	recalls = list()
	cnt = 0
	for line in lines:
		gt_file, pred_file = line.split()
		gt = get_gt(gt_file, anno_key, resized_height, scale_range)
		pred, probs = get_pred_txt(pred_file, is_include_cls, scale_range)
		# img_path = '/'.join(gt_file.split('/')[0:-2]) + "/JPEGImages/" + gt_file.split('/')[-1].split('.')[0] + ".jpg"

		precisions.append(list())
		recalls.append(list())
		for k in range(len(prob_thres)):
			if len(pred) > 0:
				I = probs > prob_thres[k]
				prob_k = probs[I]
				pred_k = pred[I, :]
			else:
				pred_k = []
			c = precision(pred_k, gt, iou_thres)
			precisions[-1].append(c)
			r = recall(pred_k, gt, iou_thres)
			recalls[-1].append(r)

		# show(img_path,gt,pred,probs)
		cnt += 1
		if cnt % 100 == 0:
			print "precessed {}".format(cnt)

	precisions = np.array(precisions)
	recalls = np.array(recalls)

	roc_save_dir = "{}/roc".format(save_dir)
	if os.path.exists(roc_save_dir):
		shutil.rmtree(roc_save_dir)
	os.mkdir(roc_save_dir)

	np.save("%s/precision_iou%.3f.npy" % (roc_save_dir, iou_thres), precisions)
	np.save("%s/recall_iou%.3f.npy" % (roc_save_dir, iou_thres), recalls)

	mean_p = np.mean(precisions, axis=0)
	mean_r = np.mean(recalls, axis=0)
	return (mean_p, mean_r)


def get_gt_pred_file(gt_path, pred_dir, save_dir):
	lines = open(gt_path, 'r').readlines()
	gt_pred_file = "{}/gt_pred_file".format(save_dir)
	f = open(gt_pred_file, 'w')
	for line in lines:
		lst = line.split()
		if len(lst) == 1:
			line = line.strip()
		else:
			line = line.split()[1].strip()
		anno_name = line.split('/')[-1].split('.')[0] + ".txt"
		f.write("{} {}/{}\n".format(line, pred_dir, anno_name))
	f.close()

	return gt_pred_file


def parse_args():
	parser = argparse.ArgumentParser(description='roc')
	parser.add_argument('--anno_file', dest='anno_file', help='gt file path', type=str)
	parser.add_argument('--save_dir', dest='save_dir', help='save dir', type=str)
	parser.add_argument('--anno_key', dest='anno_key', help='h5 file dataset key, use it to get gt', type=str)
	parser.add_argument('--resized_height', dest='resized_height', default=None, help='img height when test',
						type=float)
	parser.add_argument('--ious', dest='ious', default="(0.3,0.4)", help='ious to compute roc, should be tuple or list',
						type=str)
	parser.add_argument('--scale_ranges', dest='scale_ranges', default="(0,1000)",
						help='split range scales to compute roc, "(s1,s2),(s3,s4),..."',
						type=str)
	parser.add_argument('--include_cls', dest='include_cls', help='flag to note whether include cls in pred_file',
						action='store_true')
	parser.add_argument('--show', dest='show', help='whether to show plot figure',
						action='store_true')

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	args = parser.parse_args()
	return args


def get_title(save_dir):
	lst = os.path.abspath(save_dir).split('/')
	index = lst.index('jobs')
	title_str = '/'.join(lst[index - 1:])
	return title_str


if __name__ == "__main__":
	args = parse_args()

	pred_dir = "{}/preds".format(args.save_dir)
	gt_pred_file = get_gt_pred_file(args.anno_file, pred_dir, args.save_dir)
	scale_range_list = eval(args.scale_ranges) #(10, 1000)
	if not isinstance(scale_range_list[0], list) and not isinstance(scale_range_list[0], tuple):
		scale_range_list = (scale_range_list,)

	iou_list = eval(args.ious)
	if not isinstance(iou_list, list) and not isinstance(iou_list, tuple):
		iou_list = (iou_list,)

	plt.figure(figsize=(8, 7))
	stats = []
	for iou_thres in iou_list:
		for scale_range in scale_range_list:
			mean_p, mean_r = roc(gt_pred_file, args.save_dir, args.anno_key, iou_thres, args.include_cls,
								 args.resized_height, scale_range)
			stats.append([mean_p, mean_r])
	for mean_p, mean_r in stats:
		plt.plot(mean_p, mean_r, 'o-')
		plt.hold(True)
	plt.hold(False)
	plt.grid(True)
	plt.xlim([0, 1])
	plt.ylim([0, 1])
	plt.xlabel("precision")
	plt.ylabel("recall")
	plt.title(get_title(args.save_dir))

	plt.legend(
		['iou: {} scale: [{}, {}]'.format(iou_thres, scale_range[0], scale_range[1]) for iou_thres in iou_list for
		 scale_range in scale_range_list], loc="lower left")
	plt.savefig("{}/roc/roc.png".format(args.save_dir))
	if args.show:
		plt.show()
