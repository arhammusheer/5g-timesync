import { DatapointV2, PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

const CURRENT_DEVICE = 9;

const ensureDevice = async () => {
  const device = await prisma.deviceV2.findUnique({
    where: {
      id: CURRENT_DEVICE,
    },
  });

  if (!device) {
    await prisma.deviceV2.create({
      data: {
        id: CURRENT_DEVICE,
        name: `Device ${CURRENT_DEVICE}`,
      },
    });
  }
};

const dataFromFile = (file: string): DatapointV2[] => {
  const data = require(file);

  return data.map((item: any) => {
    return {
      device_id: CURRENT_DEVICE,
      ...item,
    };
  });
};

async function uploadData(data: DatapointV2[]) {
  await prisma.datapointV2.createMany({
    data: data,
  });
}

const main = async () => {
  await ensureDevice();
  const data = dataFromFile(`./data/${CURRENT_DEVICE}.json`);
  await uploadData(data);
};

main()
  .catch((e) => {
    throw e;
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
