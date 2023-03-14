# Specify the base image for the environment
FROM mhubai/base:cuda12.0

# Install TotalSegmentator
RUN pip3 install --no-cache-dir monai[ignite] fire
# Pull monai bundle 
ARG BUNDLE_URL="https://github.com/Project-MONAI/model-zoo/releases/download/hosting_storage_v1/spleen_ct_segmentation_v0.3.8.zip"

WORKDIR /app/bundle
RUN wget ${BUNDLE_URL} -O "temp.zip"
RUN unzip "temp.zip" -d /app/bundle
RUN rm "temp.zip"

# Move all bundle files to root
RUN mv */* .

# Default run script
CMD ["python3", "/app/mhub/monai_spleen_bundle/scripts/run.py"]