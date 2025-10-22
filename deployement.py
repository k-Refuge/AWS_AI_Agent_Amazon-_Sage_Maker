import boto3
from sagemaker.model import Model

role = "arn:aws:iam::745039059599:role/service-role/AmazonSageMakerExecutionRole"

# Create the SageMaker model
model = Model(
    image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:2.0.0-cpu-py310",
    model_data=None,  # no static ML model
    role=role,
    entry_point="inference.py",  # inference script
    source_dir=".",              # the folder that contains your code
    env={
        "AWS_DEFAULT_REGION": "us-east-1",
        "VECTOR_STORE_PATH": "/opt/ml/model/faiss_index"
    }
)

# Deploy an HTTP endpoint
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name="juridique-rag-agent"
)

