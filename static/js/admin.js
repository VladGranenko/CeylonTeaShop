
            /* CHANGE COLOR EXCEL BTN */
document.addEventListener('DOMContentLoaded', function() {
    const fileExcelLabel = document.querySelector(".btn-load-excel-label");
    const fileExcelInput = document.querySelector('.btn-load-excel');
    const btnDownloadExcel = document.querySelector(".btn-download-excel");

    fileExcelInput.addEventListener('change', () => {
        fileExcelLabel.style.color = 'rgb(255, 72, 0)';
    });
});