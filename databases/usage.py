from ZODB import FileStorage, DB
import transaction
from proyek import Proyek

# Create a ZODB database and storage
storage = FileStorage.FileStorage("proyek.fs")
db = DB(storage)
connection = db.open()
root = connection.root

# Create an instance of the Proyek class
proyek = Proyek()

# Add data to the Proyek object
data_entry1 = {
    "SIbol": "Sibol",
    "NAMA": "REMLYANA LUMBAN GAOL",
    "JK": "Wanita",
    "JURUSAN": "CS/WANITA",
    "PANJANG": 62,
    "BAHU": 39,
    # Add more fields here
}
data_entry2 = {
    "SIbol": "Sibol",
    "NAMA": "John Doe",
    "JK": "Pria",
    "JURUSAN": "CS/PRIA",
    "PANJANG": 70,
    "BAHU": 42,
    # Add more fields here
}
proyek.add_data(data_entry1)
proyek.add_data(data_entry2)


# Filter the data using all fields (case insensitive and exact match)
all_filtered_data = proyek.filter()

# Filter the data using the 'JK' field with value 'Wanita' (case insensitive and exact match)
jk_filtered_data = proyek.filter(field="JK", value="Wanita")

# Filter the data using the 'NAMA' field with value 'lumban' (case insensitive and substring match)
nama_filtered_data = proyek.filter(field="NAMA", value="lumban", exact=True)


# Sort the data based on the 'NAMA' field in ascending order
proyek.sort(field="NAMA", ascending=True)

# Get the sorted data
sorted_data = proyek.get_data()


limited_data = sorted_data[:3]

# Store the Proyek object in the root of the ZODB
root["proyek"] = proyek

# Paginate the data with page size 1 and page number 2
page_size = 1
page_number = 2
paginated_data = proyek.paginate(page_size, page_number)

# Print the paginated data
for entry in paginated_data:
    print(entry)

# Commit the changes and close the connection
transaction.commit()
connection.close()
db.close()
