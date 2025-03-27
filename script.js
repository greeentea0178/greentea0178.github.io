// スムーズスクロール
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// フォーム送信
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // フォームデータの取得
        const formData = new FormData(this);
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });

        // ここにフォーム送信のロジックを追加
        // 例: APIエンドポイントへの送信など
        console.log('フォームデータ:', formObject);
        
        // 送信成功時の処理
        alert('お問い合わせありがとうございます。\n後ほどご連絡させていただきます。');
        this.reset();
    });
}

// スクロール時のヘッダー表示/非表示
let lastScroll = 0;
const header = document.querySelector('header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        header.classList.remove('scroll-up');
        return;
    }
    
    if (currentScroll > lastScroll && !header.classList.contains('scroll-down')) {
        // 下スクロール
        header.classList.remove('scroll-up');
        header.classList.add('scroll-down');
    } else if (currentScroll < lastScroll && header.classList.contains('scroll-down')) {
        // 上スクロール
        header.classList.remove('scroll-down');
        header.classList.add('scroll-up');
    }
    lastScroll = currentScroll;
});

// Markdownファイルを読み込んで表示
async function loadDiaryEntries() {
    try {
        // diaryフォルダ内のファイル一覧を取得するためのAPIエンドポイントが必要です
        const response = await fetch('/api/diary-entries');
        const entries = await response.json();
        
        const diaryContainer = document.getElementById('diary-container');
        
        // 日付順に並び替え（新しい順）
        entries.sort((a, b) => new Date(b.date) - new Date(a.date));
        
        for (const entry of entries) {
            const entryResponse = await fetch(`/diary/${entry.filename}`);
            const entryContent = await entryResponse.text();
            
            const entryDiv = document.createElement('div');
            entryDiv.className = 'diary-entry';
            entryDiv.innerHTML = entryContent;
            
            diaryContainer.appendChild(entryDiv);
        }
    } catch (error) {
        console.error('日記エントリーの読み込みに失敗しました:', error);
    }
}

// ページ読み込み時に実行
document.addEventListener('DOMContentLoaded', loadDiaryEntries);

document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('active');  // ハンバーガーアイコンの状態も変更
    });
}); 
