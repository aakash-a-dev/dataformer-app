FROM dataformer/dfapp:0.0.1

CMD ["python", "-m", "dfapp", "run", "--host", "0.0.0.0", "--port", "7860"]
