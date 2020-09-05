from pathlib import Path
from warnings import warn

from lime import dump as limeDump
from plumbum import cli

from . import blobToWriteCommands


class HCD2LiMECLI(cli.Application):
	"""Converts an *.hcd file for Cypress chips into LiME memory dump representing the writes found in the dump"""

	format = cli.switches.SwitchAttr(["-f", "--format"], help="Format of the dump")
	allowNonPatchram = cli.switches.Flag(["--allow-non-patchram"], help="Allow non-patchram HCI commands.")

	def main(self, dumpFile="./bcm4334.hcd"):
		hcdF = Path(dumpFile)

		if self.allowNonPatchram:

			def processInvalid(i, c):
				if c.opcode.group != c.Group.vendor_specific:
					warn("Command " + repr(i) + " is not vendor-specific: " + repr(c.opcode.group) + " " + repr(c.opcode.command))
				else:
					vSC = c.parameters.payload
					warn("Command " + repr(i) + " is not used for patchram: " + repr(vSC.command))

		else:

			def processInvalid(i, c):
				if c.opcode.group != c.Group.vendor_specific:
					raise ValueError("Command " + repr(i) + " is not vendor-specific: " + repr(c.opcode.group) + " " + repr(c.opcode.command), c)
				else:
					vSC = c.parameters.payload
					raise ValueError("Command " + repr(i) + " is not used for patchram: " + repr(vSC.command), c)

		data2up = list(blobToWriteCommands(hcdF.read_bytes(), processInvalid))
		outFile = hcdF.parent / (hcdF.name + ".lime")
		with outFile.open("wb") as of:
			limeDump(data2up, of)


if __name__ == "__main__":
	HCD2LiMECLI.run()
