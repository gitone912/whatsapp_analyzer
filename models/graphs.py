from io import StringIO
import numpy as np
import matplotlib.pyplot as plt
from models import process


def return_graph():
    x = np.arange(0,np.pi*3,.1)
    y = np.sin(x)
    fig = plt.figure()
    plt.hist(x,y)
    imgdata=StringIO()
    fig.savefig(imgdata,format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data
    
