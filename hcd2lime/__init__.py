def blobToWriteCommands(b, invalidCallback):
	from .kaitai import parse

	return parsedToWriteCommands(parse(b), invalidCallback)


def parsedToWriteCommands(p, invalidCallback):
	for i, c in enumerate(p.commands):
		if c.opcode.group == c.Group.vendor_specific:
			vSC = c.parameters.payload
			if vSC.command == vSC.Command.write_ram:
				pld = vSC.payload
				yield (pld.address, pld.data)
				continue
			elif vSC.command == vSC.Command.launch_ram:
				yield None

		invalidCallback(i, c)
