FROM gcr.io/tensorflow/tensorflow
   #Install packages
   RUN DEBIAN_FRONTEND=noninteractive apt-get update
   RUN DEBIAN_FRONTEND=noninteractive apt-get -qqy install wget python-pip git timidity unzip
   RUN DEBIAN_FRONTEND=noninteractive pip install --upgrade pip
   RUN DEBIAN_FRONTEND=noninteractive pip install tqdm pandas seaborn bokeh sklearn keras h5py scikit-image
   RUN DEBIAN_FRONTEND=noninteractive pip install git+https://github.com/tflearn/tflearn.git

   RUN pip install --upgrade numpy
   RUN pip install --upgrade scikit-image

   #Remove examples
   RUN rm -Rf *