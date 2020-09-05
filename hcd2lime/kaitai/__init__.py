from io import BytesIO

from kaitaistruct import KaitaiStream

from .bluetooth_hcd import BluetoothHcd
from .bluetooth_vendors_ids import BluetoothVendorsIds


def parse(hcdBin):
	if isinstance(hcdBin, (bytes, bytearray)):
		iO = BytesIO(hcdBin)
	return BluetoothHcd(BluetoothVendorsIds.Vendor.cypress_semiconductor, KaitaiStream(iO))
