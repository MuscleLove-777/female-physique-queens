// ============================================
// FEMALE PHYSIQUE QUEENS - Script
// ============================================

document.addEventListener('DOMContentLoaded', () => {

    // --- カテゴリフィルター ---
    const filterBtns = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.athlete-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // アクティブボタン切り替え
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.dataset.filter;

            let visibleIndex = 0;
            cards.forEach((card) => {
                const categories = card.dataset.category.split(' ');
                if (filter === 'all' || categories.includes(filter)) {
                    card.classList.remove('hidden');
                    card.style.animation = 'none';
                    card.offsetHeight; // reflow
                    card.style.animation = `fadeInUp 0.5s ease ${visibleIndex * 0.05}s forwards`;
                    visibleIndex++;
                } else {
                    card.classList.add('hidden');
                }
            });

            // カウンター更新
            const visible = document.querySelectorAll('.athlete-card:not(.hidden)').length;
            document.getElementById('athleteCount').textContent = visible;
        });
    });

    // --- スクロールでヒーローフェード ---
    const hero = document.querySelector('.hero');
    const heroContent = document.querySelector('.hero-content');

    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        const heroHeight = hero.offsetHeight;
        if (scrollY < heroHeight) {
            const opacity = 1 - (scrollY / heroHeight) * 1.5;
            const translateY = scrollY * 0.3;
            heroContent.style.opacity = Math.max(0, opacity);
            heroContent.style.transform = `translateY(${translateY}px)`;
        }
    });

    // --- スムーズスクロール（スクロールインジケーター） ---
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', () => {
            const filterNav = document.querySelector('.filter-nav');
            filterNav.scrollIntoView({ behavior: 'smooth' });
        });
        scrollIndicator.style.cursor = 'pointer';
    }

});
