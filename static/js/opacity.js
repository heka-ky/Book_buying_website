let currentIndex = 0;  
const items = document.querySelectorAll('#carousel .carousel-item');  
const itemCount = items.length;  
  
function carousel() {  
    items.forEach((item, index) => {  
        item.style.opacity = index === currentIndex ? 1 : 0;  
    });  
  
    currentIndex = (currentIndex + 1) % itemCount; // 更新索引并循环  
  
    // 使用setTimeout来创建轮播效果  
    setTimeout(carousel, 3000); // 每3秒轮播一次  
}  
  
// 启动轮播  
carousel();