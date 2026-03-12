import mlflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("my-first-experiment")
def metric1():
    with mlflow.start_run():
        mlflow.log_metric("accuracy", 0.95)
        mlflow.log_metric("precision", 0.92)
        mlflow.log_metric("recall", 0.90)

def metric2():
    with mlflow.start_run():
        mlflow.log_metric("accuracy", 0.76)
        mlflow.log_metric("precision", 0.73)
        mlflow.log_metric("recall", 0.71)

if __name__ == "__main__":
    metric1()
    metric2()
