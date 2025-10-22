import boto3
from sagemaker.model import Model

role = "arn:aws:iam::745039059599:role/service-role/AmazonSageMakerExecutionRole"

# 1️⃣ Créer le modèle SageMaker
model = Model(
    image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:2.0.0-cpu-py310",
    model_data=None,  # pas de modèle ML statique
    role=role,
    entry_point="inference.py",  # le script d’inférence
    source_dir=".",              # le dossier contenant ton code
    env={
        "AWS_DEFAULT_REGION": "us-east-1",
        "VECTOR_STORE_PATH": "/opt/ml/model/faiss_index"
    }
)

# 2️⃣ Déployer un endpoint HTTP
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name="juridique-rag-agent"
)
