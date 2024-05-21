import traceback
from pyVim import connect
from pyVmomi import vim

# Function to create VMs with enhanced error handling
def create_vm(vm_name, template, folder, datacenter, cluster, networks):
    try:
        spec = vim.vm.CloneSpec()
        spec.location = vim.vm.RelocateSpec(pool=cluster.resourcePool)
        spec.powerOn = True
        spec.template = False

        task = template.Clone(name=vm_name, folder=folder, spec=spec)
        print("Creating VM '{}'...".format(vm_name))
        task_info = vim.Task.WaitForTask(task)
        if task_info.state == 'success':
            print("VM '{}' created successfully.".format(vm_name))
        else:
            print("Failed to create VM '{}': {}".format(vm_name, task_info.error))
    except Exception as e:
        print("Error creating VM '{}': {}".format(vm_name, str(e)))
        traceback.print_exc()

# Loop to create multiple VMs
for i in range(1, 3): # Change 3 to the desired number of VMs
    vm_name = "cf-pctest{:02d}".format(i)
    template = content.rootFolder.find_by_inventory_path("/Rockville Datacenter/vm/cf-pc02.ubuntu.template")
    folder = datacenter.vmFolder
    cluster = datacenter.hostFolder.childEntity[0] # Assuming the first cluster is used
    networks = [vim.Network("Compfinity Network")]

    create_vm(vm_name, template, folder, datacenter, cluster, networks)

# Close connection
connect.Disconnect(service_instance)