import yoda
# import rivet
import matplotlib.pylab as plt


yoda_file='test_pre.yoda'
yoda_object=yoda.read(yoda_file)
# print('FILE OBJECTS:',yoda_object,'\n')
print(yoda_object)
# for key, val in yoda_object.items():
#     print(key, val)
# print(yoda_object)
myh2='/RAW/RIVET_NTUPLIZER/myh2'
myh2=yoda_object[myh2]

# print('HIST OBJECT', yoda_object[hist])
plt.step(myh2.xMaxs(), myh2.yVals())
plt.show()








color_palettes={"blue":["#084594","#2171b5","#4292c6","#6baed6","#9ecae1","#c6dbef","#eff3ff"],
                "red":["#99000d","#cb181d","#ef3b2c","#fb6a4a","#fc9272","#fcbba1","#fee5d9"],
                "green":["#005a32","#238b45","#41ab5d","#74c476","#a1d99b","#c7e9c0","#edf8e9"],
                "purple":["#4a1486","#6a51a3","#807dba","#9e9ac8","#bcbddc","#dadaeb","#f2f0f7"],
                "orange":["#8c2d04","#d94801","#f16913","#fd8d3c","#fdae6b","#fdd0a2","#feedde"],
                "black":["#252525","#525252","#737373","#969696","#bdbdbd","#d9d9d9","#f7f7f7"]}