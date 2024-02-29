// Load data onto prisma

import { Datapoint, PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function uploadData(data: Datapoint[]) {
  await prisma.datapoint.createMany({
		data: data,
	});
}


const CURRENT_DEVICE = 3;

const dataFromFile = (file: string): Datapoint[] => {
  const data = require(file);

  return data.map((item: any) => {
    return {
      device_id: CURRENT_DEVICE,
      ...item,
    };
  });
};

const ensureDevice = async () => {
	const device = await prisma.device.findUnique({
		where: {
			id: CURRENT_DEVICE,
		},
	});

	if (!device) {
		await prisma.device.create({
			data: {
				id: CURRENT_DEVICE,	
				name: "Device 0",
			},

		});
	}
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
