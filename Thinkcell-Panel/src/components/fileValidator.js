// Validates whether input files are in correct format

export function handleKeyFileChange(e) {
    const file = e.target.files[0]
    if (file) {
        const fileName = file.name.toLowerCase();
        if (!(fileName.endsWith('.ppttc') || fileName.endsWith('.csv'))) {
            alert("Invalid file type. Please upload a .ptpttc or .csv file.");
            e.target.value = "";
        }
    }
}

export function handleTemplateFileChange(e) {
    const file = e.target.files[0]
    if (file) {
        const fileName = file.name.toLowerCase();
        if (!(fileName.endsWith('.ppttc'))) {
            alert("Invalid file type. Please upload a .ppttc file.");
            e.target.value = "";
        }
    }
}