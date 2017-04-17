from fuzzywuzzy import fuzz
import numpy as np

def rule_brand_logo(brand_1, brand_2, brand_3, logo_pred):
	ratio1 = fuzz.partial_ratio(logo_pred, brand_1)
	ratio2 = fuzz.partial_ratio(logo_pred, brand_2)
	ratio3 = fuzz.partial_ratio(logo_pred, brand_3)

	if ((ratio1 >= 80) or (ratio2 >= 80) or (ratio3 >= 80)):        
	    check = (brand_1, ratio1)
	    if ratio2 > check[1]:
	        check = (brand_2,ratio2)
	    if ratio3 > check[1]:
	        check = (brand_3,ratio3)

		return check[0]
	else:
		return 'null'

def rule_tag_logo(tag_1, tag_2, tag_3, logo_pred):
	ratio1 = fuzz.partial_ratio(logo_pred, tag_1)
	ratio2 = fuzz.partial_ratio(logo_pred, tag_2)
	ratio3 = fuzz.partial_ratio(logo_pred, tag_3)

	if ((ratio1 >= 80) or (ratio2 >= 80) or (ratio3 >= 80)):
		check = (tag_1, ratio1)
		if ratio2 > check[1]:
			check = (tag_2,ratio2)
		if ratio3 > check[1]:
			check = (tag_3,ratio3)

		return check[0]
	else:
		return 'null'

def rule_ocr_tag(brand_1, brand_2, brand_3, tag_1, tag_2, tag_3):
	var1, var2, ratio = dict(), dict(), dict()

	var1[0] = brand_1
	var1[1] = brand_2
	var1[2] = brand_3

	var2[0] = tag_1
	var2[1] = tag_2
	var2[2] = tag_3

	if ((var1[0] == 'null') or (var2[0] == 'null')):
		pred.loc[i, 'rule3_ocr_tag'] = 'null'
		pred.loc[i, 'rule3'] = 'null'
	else:
		for key1, ocr in var1.iteritems():
			top = 0
			for key2, tag in var2.iteritems():
				num = fuzz.partial_ratio(ocr, tag)
				if num > top:
					top = num
			ratio[key1] = top
		
		rank = np.argmax([ratio[0], ratio[1], ratio[2]])
		
		if ratio[rank] >= 100:
			return var1[rank]
		else:
			return 'null'

