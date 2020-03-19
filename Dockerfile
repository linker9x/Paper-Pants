# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8



# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt . 
RUN pip3 install -r requirements.txt

WORKDIR /app
ADD . /app

# During debugging, this entry point will be overridden. For more information, refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "paper_pants/experiments.py"]
