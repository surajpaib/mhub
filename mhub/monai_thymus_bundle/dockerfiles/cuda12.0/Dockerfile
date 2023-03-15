# Specify the base image for the environment
FROM mhubai/base:cuda12.0

# Install TotalSegmentator
RUN pip3 install --no-cache-dir monai[ignite] fire psutil
# Pull monai bundle 
ARG BUNDLE_URL="https://transfer.sh/pOVPV8/anterior-mediastinum.zip"

WORKDIR /app/bundle
RUN wget ${BUNDLE_URL} -O "temp.zip"
RUN unzip "temp.zip" -d /app/bundle
RUN rm "temp.zip"

# Move all bundle files to root
RUN mv bundle/* .

# Default run script
CMD ["python3", "/app/mhub/monai_thymus_bundle/scripts/run.py"]