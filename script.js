// Application State
const appState = {
    currentPage: 'page-select',
    selectedTemplate: null,
    cardData: {
        to: '亲爱的你',
        message: '愿新的一年\n所有美好如约而至',
        from: '来自远方'
    }
};

// DOM Elements
const elements = {
    pageSelect: document.getElementById('page-select'),
    pageEdit: document.getElementById('page-edit'),
    pageSeal: document.getElementById('page-seal'),
    pageDelivery: document.getElementById('page-delivery'),
    templateItems: document.querySelectorAll('.template-item'),
    cardInnerImage: document.getElementById('cardInnerImage'),
    inputTo: document.getElementById('inputTo'),
    inputMessage: document.getElementById('inputMessage'),
    inputFrom: document.getElementById('inputFrom'),
    previewTo: document.getElementById('previewTo'),
    previewMessage: document.getElementById('previewMessage'),
    previewFrom: document.getElementById('previewFrom'),
    countTo: document.getElementById('countTo'),
    countMessage: document.getElementById('countMessage'),
    countFrom: document.getElementById('countFrom'),
    btnBack: document.getElementById('btnBack'),
    btnComplete: document.getElementById('btnComplete'),
    animationStage: document.getElementById('animationStage'),
    sealAction: document.getElementById('sealAction'),
    btnSend: document.getElementById('btnSend'),
    modalSend: document.getElementById('modal-send'),
    inputEmail: document.getElementById('inputEmail'),
    btnCancelSend: document.getElementById('btnCancelSend'),
    btnConfirmSend: document.getElementById('btnConfirmSend'),
    deliveryText: document.getElementById('deliveryText'),
    horseContainer: document.getElementById('horseContainer'),
    progressOverlay: document.getElementById('progress-overlay'),
    progressBar: document.getElementById('progressBar'),
    progressText: document.getElementById('progressText'),
    cardCanvas: document.getElementById('cardCanvas')
};

// Utility Functions
function adjustMessageFontSize(text) {
    const length = text.length;
    let fontSize;
    
    // 根据字数动态调整字体大小
    if (length <= 20) {
        fontSize = '2rem';      // 20字以内：最大字体
    } else if (length <= 40) {
        fontSize = '1.7rem';    // 20-40字：稍小
    } else if (length <= 60) {
        fontSize = '1.5rem';    // 40-60字：中等
    } else if (length <= 80) {
        fontSize = '1.3rem';    // 60-80字：较小
    } else if (length <= 100) {
        fontSize = '1.15rem';   // 80-100字：小
    } else if (length <= 120) {
        fontSize = '1.05rem';   // 100-120字：更小
    } else {
        fontSize = '0.95rem';   // 120字以上：最小
    }
    
    elements.previewMessage.style.setProperty('--message-font-size', fontSize);
}

function switchPage(fromPage, toPage) {
    const from = document.getElementById(fromPage);
    const to = document.getElementById(toPage);
    
    from.classList.add('exit');
    
    setTimeout(() => {
        from.classList.remove('active', 'exit');
        to.classList.add('active');
        appState.currentPage = toPage;
    }, 400);
}

function updateCharCount(input, counter) {
    const count = input.value.length;
    counter.textContent = count;
}

// 截图贺卡预览生成base64图片
async function captureCardPreview() {
    try {
        const cardCanvas = elements.cardCanvas;
        const rect = cardCanvas.getBoundingClientRect();
        
        // 创建canvas
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // 设置canvas尺寸，使用更高的分辨率
        const scale = 3; // 提高到3倍分辨率以获得更清晰的图片
        canvas.width = rect.width * scale;
        canvas.height = rect.height * scale;
        ctx.scale(scale, scale);
        
        // 绘制背景图
        const bgImg = elements.cardInnerImage;
        
        // 等待图片加载完成
        if (!bgImg.complete) {
            await new Promise((resolve, reject) => {
                bgImg.onload = resolve;
                bgImg.onerror = reject;
                setTimeout(reject, 5000); // 5秒超时
            });
        }
        
        // 绘制背景图片
        ctx.drawImage(bgImg, 0, 0, rect.width, rect.height);
        
        // 获取文字叠加层的实际渲染样式
        const textOverlay = cardCanvas.querySelector('.card-text-overlay');
        const textGroup = textOverlay.querySelector('.text-group');
        const computedStyle = window.getComputedStyle(textGroup);
        
        // 获取文字元素
        const toElement = elements.previewTo;
        const messageElement = elements.previewMessage;
        const fromElement = elements.previewFrom;
        
        // 获取实际计算的样式
        const toStyle = window.getComputedStyle(toElement);
        const messageStyle = window.getComputedStyle(messageElement);
        const fromStyle = window.getComputedStyle(fromElement);
        
        // 设置阴影效果
        ctx.shadowColor = 'rgba(255, 255, 255, 0.9)';
        ctx.shadowBlur = 8;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 2;
        
        // 绘制"致"文字
        const toText = toElement.textContent;
        const toFontSize = parseFloat(toStyle.fontSize);
        const toColor = toStyle.color;
        
        ctx.font = `bold ${toFontSize}px KaiTi, STKaiti, "华文楷体", serif`;
        ctx.fillStyle = toColor;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        
        const toY = rect.height * 0.18;
        ctx.fillText(toText, rect.width / 2, toY);
        
        // 绘制祝福语（处理换行）
        const messageText = messageElement.textContent;
        const messageFontSizeStr = messageStyle.getPropertyValue('--message-font-size') || messageStyle.fontSize;
        const messageFontSize = parseFloat(messageFontSizeStr);
        const messageColor = messageStyle.color;
        
        ctx.font = `${messageFontSize}px KaiTi, STKaiti, "华文楷体", serif`;
        ctx.fillStyle = messageColor;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        
        const lines = messageText.split('\n');
        const lineHeight = messageFontSize * 1.6;
        const totalHeight = lines.length * lineHeight;
        const startY = (rect.height - totalHeight) / 2 + rect.height * 0.08;
        
        lines.forEach((line, index) => {
            if (line.trim()) {
                ctx.fillText(line, rect.width / 2, startY + index * lineHeight);
            }
        });
        
        // 绘制署名
        const fromText = fromElement.textContent;
        const fromFontSize = parseFloat(fromStyle.fontSize);
        const fromColor = fromStyle.color;
        
        ctx.font = `italic ${fromFontSize}px KaiTi, STKaiti, "华文楷体", serif`;
        ctx.fillStyle = fromColor;
        ctx.textAlign = 'right';
        ctx.textBaseline = 'bottom';
        ctx.shadowBlur = 8; // 恢复阴影
        
        const fromY = rect.height * 0.88;
        const fromX = rect.width * 0.92;
        ctx.fillText(fromText, fromX, fromY);
        
        // 转换为base64
        const base64Data = canvas.toDataURL('image/png', 0.95);
        console.log('贺卡截图成功，图片大小:', base64Data.length, 'bytes');
        return base64Data;
        
    } catch (error) {
        console.error('截图失败:', error);
        // 如果截图失败，返回null让后端使用原始图片
        return null;
    }
}

// Template Selection
console.log('Initializing template selection...');

elements.templateItems.forEach((item, index) => {
    const img = item.querySelector('.template-cover');
    
    if (!img) {
        console.error('Image not found for template item:', index);
        return;
    }
    
    const staticSrc = img.src;
    const gifSrc = img.getAttribute('data-gif');
    
    console.log(`Template ${index + 1}:`, { staticSrc, gifSrc });
    
    // Mouse enter - switch to GIF
    item.addEventListener('mouseenter', () => {
        console.log(`Hover on template ${index + 1} - switching to GIF:`, gifSrc);
        img.src = gifSrc;
    });
    
    // Mouse leave - switch back to static
    item.addEventListener('mouseleave', () => {
        console.log(`Leave template ${index + 1} - switching to static:`, staticSrc);
        img.src = staticSrc;
    });
    
    // Click to select template
    item.addEventListener('click', () => {
        const templateId = item.dataset.template;
        appState.selectedTemplate = templateId;
        elements.cardInnerImage.src = `cards/${templateId.padStart(2, '0')}_inner page.png`;
        switchPage('page-select', 'page-edit');
    });
});

console.log('Template selection initialized!');

// Edit Page
elements.inputTo.addEventListener('input', (e) => {
    appState.cardData.to = e.target.value;
    elements.previewTo.textContent = e.target.value || '亲爱的你';
    updateCharCount(elements.inputTo, elements.countTo);
});

elements.inputMessage.addEventListener('input', (e) => {
    appState.cardData.message = e.target.value;
    elements.previewMessage.textContent = e.target.value || '愿新的一年\n所有美好如约而至';
    updateCharCount(elements.inputMessage, elements.countMessage);
    adjustMessageFontSize(e.target.value);
});

elements.inputFrom.addEventListener('input', (e) => {
    appState.cardData.from = e.target.value;
    elements.previewFrom.textContent = e.target.value || '来自远方';
    updateCharCount(elements.inputFrom, elements.countFrom);
});

updateCharCount(elements.inputTo, elements.countTo);
updateCharCount(elements.inputMessage, elements.countMessage);
updateCharCount(elements.inputFrom, elements.countFrom);
adjustMessageFontSize(elements.inputMessage.value);

elements.btnBack.addEventListener('click', () => {
    switchPage('page-edit', 'page-select');
});

elements.btnComplete.addEventListener('click', () => {
    switchPage('page-edit', 'page-seal');
    setTimeout(() => {
        playSealAnimation();
    }, 500);
});

// Seal Animation - 自动播放
let currentSealStep = 0;

function playSealAnimation() {
    const stage = elements.animationStage;
    stage.innerHTML = '';
    currentSealStep = 0;
    
    // 使用封面图片
    const templateId = appState.selectedTemplate.padStart(2, '0');
    const coverImageSrc = `cards/${templateId}_cover.png`;
    
    // 创建贺卡（在中间）
    const cardEl = document.createElement('div');
    cardEl.className = 'card-element';
    cardEl.innerHTML = `<img src="${coverImageSrc}" alt="Card">`;
    stage.appendChild(cardEl);
    
    // 1. 等待0.5秒，让用户看到贺卡
    setTimeout(() => {
        // 创建信封（从下方出现，盖子打开）
        const envelopeEl = document.createElement('div');
        envelopeEl.className = 'envelope-element';
        envelopeEl.innerHTML = `
            <div class="envelope-body"></div>
            <div class="envelope-flap"></div>
        `;
        stage.appendChild(envelopeEl);
        
        // 2. 信封向上移动，把贺卡吃进去（1秒后开始，持续1.2秒）
        setTimeout(() => {
            envelopeEl.style.animation = 'envelopeEatCard 1.2s ease-in-out forwards';
        }, 1000);
        
        // 3. 信封盖子关闭（2.5秒后）
        setTimeout(() => {
            const flap = envelopeEl.querySelector('.envelope-flap');
            if (flap) {
                flap.classList.add('closed');
            }
        }, 2500);
        
        // 4. 火漆印章掉落（3.5秒后）
        setTimeout(() => {
            const seal = document.createElement('div');
            seal.className = 'wax-seal';
            stage.appendChild(seal);
            seal.style.animation = 'sealDrop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards';
        }, 3500);
        
        // 5. 显示发送按钮（4.2秒后）
        setTimeout(() => {
            elements.sealAction.innerHTML = `<button class="btn btn-primary btn-large" id="btnSend">发送给好友</button>`;
            elements.sealAction.style.display = 'block';
            
            // 绑定发送按钮事件
            document.getElementById('btnSend').addEventListener('click', () => {
                elements.modalSend.classList.add('active');
                elements.inputEmail.focus();
            });
        }, 4200);
        
    }, 500);
}

function showSealStepButton(text) {
    // 这个函数现在不需要了，但保留以避免错误
}

function handleSealStep() {
    // 这个函数现在不需要了，但保留以避免错误
}


// Progress Bar Functions
let progressInterval = null;

function showProgressBar() {
    elements.progressOverlay.classList.add('active');
    elements.progressBar.style.width = '0%';
    elements.progressText.textContent = '0%';
}

function updateProgress(percent) {
    elements.progressBar.style.width = percent + '%';
    elements.progressText.textContent = Math.round(percent) + '%';
}

function hideProgressBar() {
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
    setTimeout(() => {
        elements.progressOverlay.classList.remove('active');
    }, 300);
}

// 平滑进度条动画
function startSmoothProgress(duration, callback) {
    const startTime = Date.now();
    const targetPercent = 90; // 进度到90%，最后10%等待服务器响应
    
    if (progressInterval) {
        clearInterval(progressInterval);
    }
    
    progressInterval = setInterval(() => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min((elapsed / duration) * targetPercent, targetPercent);
        
        updateProgress(progress);
        
        if (progress >= targetPercent) {
            clearInterval(progressInterval);
            progressInterval = null;
            if (callback) callback();
        }
    }, 50); // 每50ms更新一次，使动画流畅
}

// Send Modal
// 注释掉原来的btnSend监听器，按钮现在是动态创建的
// elements.btnSend.addEventListener('click', () => {
//     elements.modalSend.classList.add('active');
//     elements.inputEmail.focus();
// });

elements.btnCancelSend.addEventListener('click', () => {
    elements.modalSend.classList.remove('active');
});

elements.modalSend.querySelector('.modal-backdrop').addEventListener('click', () => {
    elements.modalSend.classList.remove('active');
});

elements.btnConfirmSend.addEventListener('click', async () => {
    const emails = elements.inputEmail.value.trim();

    if (!emails) {
        alert('请输入至少一个邮箱地址');
        return;
    }

    const emailList = emails.split(',').map(e => e.trim()).filter(e => e);
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const invalidEmails = emailList.filter(e => !emailRegex.test(e));

    if (invalidEmails.length > 0) {
        alert('请输入有效的邮箱地址');
        return;
    }

    elements.btnConfirmSend.disabled = true;
    elements.btnConfirmSend.textContent = '准备中...';

    try {
        // 关闭弹窗
        elements.modalSend.classList.remove('active');
        
        // 显示进度条并开始平滑动画（预计120秒/2分钟完成）
        showProgressBar();
        startSmoothProgress(120000);  // 120000毫秒 = 2分钟
        
        // 截图贺卡预览
        console.log('开始截取贺卡预览...');
        const cardImageBase64 = await captureCardPreview();
        console.log('贺卡预览截取完成');

        // 准备数据
        const requestData = {
            template_id: appState.selectedTemplate,
            to: appState.cardData.to,
            message: appState.cardData.message,
            from: appState.cardData.from,
            emails: emailList,
            card_preview_base64: cardImageBase64
        };

        // 发送邮件
        console.log('发送邮件请求...');
        const response = await fetch('/api/send-card', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const result = await response.json();
        console.log('服务器响应:', result);

        if (result.success) {
            // 完成进度条到100%
            updateProgress(100);
            
            // 等待进度条完成动画
            setTimeout(() => {
                hideProgressBar();
                switchPage('page-seal', 'page-delivery');
                setTimeout(() => {
                    startDeliveryAnimation(emailList);
                }, 500);
            }, 500);
        } else {
            hideProgressBar();
            alert('发送失败: ' + (result.error || '未知错误'));
        }
    } catch (error) {
        console.error('发送邮件出错:', error);
        hideProgressBar();
        alert('发送失败，请检查网络连接或后端服务是否启动');
    } finally {
        elements.btnConfirmSend.disabled = false;
        elements.btnConfirmSend.textContent = '确认寄出';
    }
});

// Delivery Animation
function startDeliveryAnimation(emailList) {
    elements.deliveryText.querySelector('.delivery-message').textContent = '马儿正在送信中……';
    
    elements.horseContainer.style.animation = 'none';
    setTimeout(() => {
        elements.horseContainer.style.animation = 'horseRun 4s linear infinite';
    }, 10);
    
    setTimeout(() => {
        elements.deliveryText.querySelector('.delivery-message').textContent = '马儿已出发，祝福已送达！';
        elements.horseContainer.style.animationPlayState = 'paused';
        
        setTimeout(() => {
            const successMessage = document.createElement('div');
            successMessage.className = 'glass-card';
            successMessage.style.marginTop = 'var(--spacing-lg)';
            successMessage.style.textAlign = 'center';
            successMessage.style.animation = 'fadeInUp 0.6s ease-out forwards';
            successMessage.innerHTML = `
                <p style="color: white; font-size: 1.25rem; margin-bottom: var(--spacing-md);">
                    已发送至 ${emailList.length} 个邮箱
                </p>
                <button class="btn btn-primary" id="btnRestart">制作新的贺卡</button>
            `;
            elements.deliveryText.appendChild(successMessage);
            
            document.getElementById('btnRestart').addEventListener('click', () => {
                location.reload();
            });
        }, 1000);
    }, 3000);
}

// Initialization
function init() {
    console.log('Page initialized!');
    setTimeout(() => {
        elements.pageSelect.classList.add('active');
    }, 100);
    
    document.querySelectorAll('input, textarea').forEach(input => {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
                e.preventDefault();
            }
        });
    });
}

// Smooth scroll
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

const originalSwitchPage = switchPage;
switchPage = function(fromPage, toPage) {
    scrollToTop();
    originalSwitchPage(fromPage, toPage);
};

// Start
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

console.log('Script loaded successfully!');