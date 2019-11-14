from cargo.services import DeliveryService, FileService

deliveryService = DeliveryService()
fileService = FileService()


def main():
    cargo = fileService.run("cargo.csv")
    truck = fileService.run("trucks.csv")
    delivery, delivery_reduced = deliveryService.run(cargo, truck)
    print(delivery)
    print('##############')
    print('Simple Result')
    print(delivery_reduced)


if __name__ == '__main__':
    main()
