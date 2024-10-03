let icons = [];

// 从JSON文件加载图标数据
fetch('levi.icons.json')
    .then(response => response.json())
    .then(data => {
        // 使用 data 进行网页的更新，例如显示图标
        console.log(data);
    })
    .catch(error => console.error('Error loading icons:', error));

function renderIcons(iconsToRender) {
    const iconGrid = document.getElementById('iconGrid');
    iconGrid.innerHTML = '';
    iconsToRender.forEach(icon => {
        const iconItem = document.createElement('div');
        iconItem.className = 'icon-item';
        iconItem.innerHTML = `
            <img src="${icon.url}" alt="${icon.name}">
            <p>${icon.name}</p>
        `;
        iconGrid.appendChild(iconItem);
    });
}

function updateCategoryFilter(icons) {
    const categoryFilter = document.getElementById('categoryFilter');
    const categories = [...new Set(icons.map(icon => icon.category).filter(Boolean))];
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        categoryFilter.appendChild(option);
    });
}

// 搜索功能
document.getElementById('search').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const filteredIcons = icons.filter(icon => 
        icon.name.toLowerCase().includes(searchTerm)
    );
    renderIcons(filteredIcons);
});

// 分类过滤
document.getElementById('categoryFilter').addEventListener('change', (e) => {
    const category = e.target.value;
    const filteredIcons = category 
        ? icons.filter(icon => icon.category === category)
        : icons;
    renderIcons(filteredIcons);
});

// 下载所有图标
document.getElementById('downloadAll').addEventListener('click', () => {
    const zip = new JSZip();
    const promises = icons.map(icon => 
        fetch(icon.url)
            .then(response => response.blob())
            .then(blob => zip.file(icon.name, blob))
    );

    Promise.all(promises).then(() => {
        zip.generateAsync({type:"blob"})
            .then(function(content) {
                const url = URL.createObjectURL(content);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'levi-icons.zip';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            });
    });
});

// 暗黑模式切换
document.getElementById('darkModeToggle').addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
});
