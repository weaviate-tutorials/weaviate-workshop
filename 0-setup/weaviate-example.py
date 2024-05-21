import weaviate
import weaviate.classes as wvc

client = weaviate.connect_to_custom(
    http_host={WEAVIATE_IP},
    http_port="8080",
    http_secure=False,
    grpc_host={WEAVIATE_IP},
    grpc_port="50051",
    grpc_secure=False
)

collection = client.collections.create(
    name="TestCollection",
    properties=[
        wvc.config.Property(
            name="title",
            data_type=wvc.config.DataType.TEXT
        )
    ]
)
print("Created collection.")
collections = client.collections.list_all()
print(collections)
client.close()