/**
 * Minimalist Client JS — House Price Estimator & Real Estate Knowledge Graph
 */

document.addEventListener('DOMContentLoaded', async () => {
    const predictionForm = document.getElementById('predictionForm');
    const submitBtn = document.getElementById('submitBtn');
    const modelSelect = document.getElementById('modelSelect');
    const presetButtons = document.querySelectorAll('.chip-btn');
    
    const singleResultCard = document.getElementById('singleResultCard');
    const comparisonCard = document.getElementById('comparisonCard');
    const mainPrice = document.getElementById('mainPrice');
    const priceM2 = document.getElementById('priceM2');
    const resultBadge = document.getElementById('resultBadge');
    
    const valArea = document.getElementById('valArea');
    const valStructure = document.getElementById('valStructure');
    const valRoads = document.getElementById('valRoads');
    const valSegment = document.getElementById('valSegment');
    
    const avgPrice = document.getElementById('avgPrice');
    const rangePrice = document.getElementById('rangePrice');
    const modelBarsContainer = document.getElementById('modelBarsContainer');

    // Real Estate KG Elements
    const tabFinanceBtn = document.getElementById('tabFinanceBtn');
    const tabGraphBtn = document.getElementById('tabGraphBtn');
    const tabFinanceContent = document.getElementById('tabFinanceContent');
    const tabGraphContent = document.getElementById('tabGraphContent');
    const amenitiesList = document.getElementById('amenitiesList');
    const bankList = document.getElementById('bankList');
    const graphCanvas = document.getElementById('knowledgeGraphCanvas');

    let presetsData = {};
    let currentGraphData = null;

    // View Mode Switcher (Desktop vs 3D Mobile App Simulator)
    const desktopModeBtn = document.getElementById('desktopModeBtn');
    const mobileModeBtn = document.getElementById('mobileModeBtn');
    const appHeaderModel = document.getElementById('appHeaderModel');

    function triggerGraphRedraw() {
        if (currentGraphData && tabGraphContent.style.display !== 'none') {
            requestAnimationFrame(() => renderKnowledgeGraph(currentGraphData));
            setTimeout(() => renderKnowledgeGraph(currentGraphData), 60);
            setTimeout(() => renderKnowledgeGraph(currentGraphData), 220);
        }
    }

    if (desktopModeBtn && mobileModeBtn) {
        desktopModeBtn.addEventListener('click', () => {
            document.body.classList.remove('mobile-device-active');
            desktopModeBtn.classList.add('active');
            mobileModeBtn.classList.remove('active');
            triggerGraphRedraw();
        });

        mobileModeBtn.addEventListener('click', () => {
            document.body.classList.add('mobile-device-active');
            mobileModeBtn.classList.add('active');
            desktopModeBtn.classList.remove('active');
            if (tabFinanceBtn) tabFinanceBtn.click();
        });
    }

    // Bottom Navigation Bar for Mobile App
    const navValuationBtn = document.getElementById('navValuationBtn');
    const navFinanceBtn = document.getElementById('navFinanceBtn');
    const reSection = document.getElementById('reSection');

    function setActiveBottomNav(btn) {
        [navValuationBtn, navFinanceBtn].forEach(b => b?.classList.remove('active'));
        btn?.classList.add('active');
    }

    if (navValuationBtn) {
        navValuationBtn.addEventListener('click', () => {
            setActiveBottomNav(navValuationBtn);
            document.querySelector('.phone-screen-container')?.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
    if (navFinanceBtn) {
        navFinanceBtn.addEventListener('click', () => {
            setActiveBottomNav(navFinanceBtn);
            if (tabFinanceBtn) tabFinanceBtn.click();
            reSection?.scrollIntoView({ behavior: 'smooth' });
        });
    }

    // 1. Fetch Presets & Models
    try {
        const [presetsRes, modelsRes] = await Promise.all([
            fetch('/api/presets'),
            fetch('/api/models')
        ]);
        const pData = await presetsRes.json();
        pData.presets.forEach(p => {
            presetsData[p.id] = p.data;
        });
        if (pData.presets.length > 0) {
            fillFormData(pData.presets[0].data);
            handlePrediction();
        }
    } catch (err) {
        console.error('Error fetching presets/models:', err);
    }

    // 2. Preset Click
    presetButtons.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            presetButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const presetId = btn.dataset.presetId;
            const data = presetsData[presetId];
            if (data) {
                fillFormData(data);
                handlePrediction();
            }
        });

        if (index === 0) {
            btn.classList.add('active');
        }
    });

    function fillFormData(data) {
        if (data.City) document.getElementById('cityInput').value = data.City;
        if (data.District) document.getElementById('districtInput').value = data.District;
        if (data.Ward) document.getElementById('wardInput').value = data.Ward;
        if (data.Area !== undefined) document.getElementById('areaInput').value = data.Area;
        if (data.Frontage !== undefined) document.getElementById('frontageInput').value = data.Frontage;
        if (data['Access Road'] !== undefined) document.getElementById('accessRoadInput').value = data['Access Road'];
        if (data.Floors !== undefined) document.getElementById('floorsInput').value = data.Floors;
        if (data.Bedrooms !== undefined) document.getElementById('bedroomsInput').value = data.Bedrooms;
        if (data.Bathrooms !== undefined) document.getElementById('bathroomsInput').value = data.Bathrooms;
        if (data['Legal status']) document.getElementById('legalSelect').value = data['Legal status'];
        if (data['Furniture state']) document.getElementById('furnitureSelect').value = data['Furniture state'];
    }

    // 3. Model Switch
    modelSelect.addEventListener('change', () => {
        if (appHeaderModel) {
            appHeaderModel.textContent = modelSelect.value === 'ALL' ? 'So sánh 5 Mô hình AI' : `${modelSelect.value} Regressor`;
        }
        handlePrediction();
    });

    // 4. Form Submit
    predictionForm.addEventListener('submit', (e) => {
        e.preventDefault();
        handlePrediction();
    });

    // 5. Tabs Control
    tabFinanceBtn.addEventListener('click', () => {
        tabFinanceBtn.classList.add('active');
        tabGraphBtn.classList.remove('active');
        tabFinanceContent.style.display = 'block';
        tabGraphContent.style.display = 'none';
    });

    tabGraphBtn.addEventListener('click', () => {
        tabGraphBtn.classList.add('active');
        tabFinanceBtn.classList.remove('active');
        tabFinanceContent.style.display = 'none';
        tabGraphContent.style.display = 'block';
        if (currentGraphData) {
            requestAnimationFrame(() => renderKnowledgeGraph(currentGraphData));
            setTimeout(() => renderKnowledgeGraph(currentGraphData), 50);
            setTimeout(() => renderKnowledgeGraph(currentGraphData), 200);
        }
    });

    function getFormPayload() {
        return {
            Area: parseFloat(document.getElementById('areaInput').value) || 50,
            Frontage: parseFloat(document.getElementById('frontageInput').value) || 0,
            'Access Road': parseFloat(document.getElementById('accessRoadInput').value) || 0,
            Floors: parseFloat(document.getElementById('floorsInput').value) || 1,
            Bedrooms: parseFloat(document.getElementById('bedroomsInput').value) || 1,
            Bathrooms: parseFloat(document.getElementById('bathroomsInput').value) || 1,
            City: document.getElementById('cityInput').value.trim() || 'Hồ Chí Minh',
            District: document.getElementById('districtInput').value.trim() || 'Gò Vấp',
            Ward: document.getElementById('wardInput').value.trim() || 'Phường 11',
            'Legal status': document.getElementById('legalSelect').value,
            'Furniture state': document.getElementById('furnitureSelect').value,
            model_name: modelSelect.value
        };
    }

    // 6. Predict Handler
    async function handlePrediction() {
        const payload = getFormPayload();
        const isAllModels = payload.model_name === 'ALL';

        submitBtn.classList.add('loading');
        submitBtn.querySelector('.btn-text').innerText = 'Đang tính toán...';

        try {
            if (isAllModels) {
                const res = await fetch('/api/predict-all', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.status === 'success') {
                    renderAllModelsResult(data);
                }
            } else {
                const res = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.status === 'success') {
                    renderSingleModelResult(data);
                    if (data.amenities) {
                        renderNearbyAmenities(data.amenities);
                    }
                    if (data.financial_package && data.financial_package.banks) {
                        renderBankLoans(data.financial_package.banks);
                    }
                    if (data.knowledge_graph) {
                        currentGraphData = data.knowledge_graph;
                        if (tabGraphContent.style.display !== 'none') {
                            requestAnimationFrame(() => renderKnowledgeGraph(currentGraphData));
                            setTimeout(() => renderKnowledgeGraph(currentGraphData), 60);
                        }
                    }
                }
            }
        } catch (err) {
            console.error('Prediction error:', err);
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.querySelector('.btn-text').innerText = 'Định giá Bất Động Sản';
        }
    }

    // 7. Render Single Result
    function renderSingleModelResult(data) {
        singleResultCard.style.display = 'block';
        comparisonCard.style.display = 'none';

        resultBadge.innerText = data.display_name;
        mainPrice.innerText = data.price_formatted;
        priceM2.innerText = data.price_per_m2_formatted;

        const areaVal = parseFloat(document.getElementById('areaInput').value) || 85;
        const floorsVal = parseInt(document.getElementById('floorsInput').value) || 3;
        const bedroomsVal = parseInt(document.getElementById('bedroomsInput').value) || 4;
        const frontageVal = parseFloat(document.getElementById('frontageInput').value) || 4.5;
        const accessRoadVal = parseFloat(document.getElementById('accessRoadInput').value) || 6.0;

        if (valArea) valArea.innerText = `${areaVal} m²`;
        if (valStructure) valStructure.innerText = `${floorsVal} Tầng • ${bedroomsVal} PN`;
        if (valRoads) valRoads.innerText = `${frontageVal}m / ${accessRoadVal}m`;

        if (valSegment) {
            let segment = "Nhà phố Đô thị";
            if (areaVal >= 200 || (data.price_billion && data.price_billion >= 15)) {
                segment = "Biệt thự Cao cấp";
            } else if (areaVal < 45) {
                segment = "Nhà ngõ diện tích nhỏ";
            }
            valSegment.innerText = segment;
        }
    }

    // 8. Render All Models Comparison
    function renderAllModelsResult(data) {
        singleResultCard.style.display = 'none';
        comparisonCard.style.display = 'block';

        avgPrice.innerText = `TB: ${data.summary.average_formatted}`;
        rangePrice.innerText = `Khoảng giá: ${data.summary.price_range}`;

        const results = data.results;
        const maxPrice = Math.max(...results.map(r => r.price_billion)) || 10;
        modelBarsContainer.innerHTML = '';
        
        results.forEach(item => {
            const percentage = maxPrice > 0 ? (item.price_billion / maxPrice) * 100 : 50;
            const barRow = document.createElement('div');
            barRow.className = `model-bar-item ${item.is_best ? 'best' : ''}`;
            barRow.innerHTML = `
                <div class="bar-row-top">
                    <span>${item.is_best ? '🏆 ' : ''}${item.display_name}</span>
                    <span>${item.price_formatted}</span>
                </div>
                <div class="bar-row-track">
                    <div class="bar-row-fill" style="width: ${percentage.toFixed(1)}%;"></div>
                </div>
                <div class="bar-row-bottom">
                    <span>Đơn giá: ${item.price_per_m2_formatted}</span>
                    <span>${item.badge || item.model_name}</span>
                </div>
            `;
            modelBarsContainer.appendChild(barRow);
        });
    }

    // 9. Render Nearby Amenities
    function renderNearbyAmenities(amenities) {
        amenitiesList.innerHTML = '';
        if (amenities && amenities.length > 0) {
            amenities.forEach(a => {
                const card = document.createElement('div');
                card.className = 'amenity-card';
                card.innerHTML = `
                    <div class="am-left">
                        <span class="am-icon">${a.icon || '📍'}</span>
                        <div>
                            <div class="am-name">${a.name}</div>
                            <div class="am-type">${a.type}</div>
                        </div>
                    </div>
                    <span class="am-dist">${a.distance}</span>
                `;
                amenitiesList.appendChild(card);
            });
        }
    }

    // 10. Render Bank Mortgage Loans
    function renderBankLoans(banks) {
        bankList.innerHTML = '';
        if (banks && banks.length > 0) {
            banks.forEach(b => {
                const m = b.mortgage || {};
                const card = document.createElement('div');
                card.className = 'bank-card';
                card.innerHTML = `
                    <div class="b-top">
                        <span class="b-name">${b.bank_name}</span>
                        <span class="b-rate">Lãi: ${b.preferential_rate_pct}%/năm</span>
                    </div>
                    <div class="b-details">
                        <span>Hạn mức: ${m.loan_amount_formatted || ''} (${b.max_ltv_pct}%)</span>
                        <span class="b-monthly">Góp: ${m.monthly_estimate_formatted || ''}</span>
                    </div>
                    <div class="b-highlight">${b.highlight || ''}</div>
                `;
                bankList.appendChild(card);
            });
        }
    }

    // 11. Knowledge Graph 2D Canvas Renderer (Normalized Proportional Coordinates)
    function renderKnowledgeGraph(graphData) {
        if (!graphCanvas || !graphData) return;
        const wrapper = document.getElementById('graphCanvasWrapper') || graphCanvas.parentElement;
        if (!wrapper) return;

        const isMobile = document.body.classList.contains('mobile-device-active') || window.innerWidth <= 820;
        
        let clientWidth = wrapper.clientWidth;
        if (!clientWidth || clientWidth < 50) {
            clientWidth = isMobile ? 330 : 920;
        }
        const clientHeight = isMobile ? 280 : 380;

        const dpr = window.devicePixelRatio || 1;
        graphCanvas.width = clientWidth * dpr;
        graphCanvas.height = clientHeight * dpr;
        graphCanvas.style.width = `${clientWidth}px`;
        graphCanvas.style.height = `${clientHeight}px`;

        const ctx = graphCanvas.getContext('2d');
        ctx.resetTransform();
        ctx.scale(dpr, dpr);
        ctx.clearRect(0, 0, clientWidth, clientHeight);

        const nodes = graphData.nodes || [];
        const edges = graphData.edges || [];

        // Normalized relative coordinates [0.12 ... 0.88]
        const padX = isMobile ? 28 : 50;
        const padY = isMobile ? 22 : 36;
        const drawW = clientWidth - 2 * padX;
        const drawH = clientHeight - 2 * padY;
        const positions = {};

        let amenityCount = 0;

        nodes.forEach((n) => {
            let rx = 0.5, ry = 0.5;
            if (n.id === 'property') {
                rx = 0.40; ry = 0.50;
            } else if (n.id === 'location') {
                rx = 0.16; ry = 0.28;
            } else if (n.id === 'valuation') {
                rx = 0.68; ry = 0.32;
            } else if (n.id === 'bank_loan') {
                rx = 0.88; ry = 0.32;
            } else if (n.id === 'broker') {
                rx = 0.68; ry = 0.74;
            } else if (n.group === 'amenity') {
                rx = 0.16;
                ry = 0.60 + amenityCount * 0.18;
                amenityCount++;
            } else {
                rx = 0.5; ry = 0.5;
            }

            positions[n.id] = {
                x: padX + rx * drawW,
                y: padY + ry * drawH
            };
        });

        // 1. Draw Edges
        edges.forEach(e => {
            const p1 = positions[e.from];
            const p2 = positions[e.to];
            if (p1 && p2) {
                ctx.beginPath();
                ctx.moveTo(p1.x, p1.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.strokeStyle = e.color || '#475569';
                ctx.lineWidth = isMobile ? 1.2 : 1.6;
                ctx.stroke();

                // Edge label
                if (!isMobile || clientWidth > 320) {
                    const midX = (p1.x + p2.x) / 2;
                    const midY = (p1.y + p2.y) / 2;
                    ctx.font = isMobile ? '7.5px Inter, sans-serif' : '9px Inter, sans-serif';
                    ctx.fillStyle = '#94a3b8';
                    ctx.textAlign = 'center';
                    ctx.fillText(e.label || '', midX, midY - 3);
                }
            }
        });

        // 2. Draw Nodes
        nodes.forEach(n => {
            const pos = positions[n.id];
            if (pos) {
                const baseR = n.size ? n.size / 2 : 12;
                const r = isMobile ? Math.max(7, baseR * 0.75) : baseR;

                // Glow ring
                ctx.beginPath();
                ctx.arc(pos.x, pos.y, r + (isMobile ? 3 : 5), 0, 2 * Math.PI);
                ctx.fillStyle = (n.color || '#2563eb') + '22';
                ctx.fill();

                // Circle body
                ctx.beginPath();
                ctx.arc(pos.x, pos.y, r, 0, 2 * Math.PI);
                ctx.fillStyle = n.color || '#2563eb';
                ctx.fill();
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = isMobile ? 1.5 : 2;
                ctx.stroke();

                // Text Label
                ctx.font = isMobile ? '8px Inter, sans-serif' : '10px Inter, sans-serif';
                ctx.fillStyle = '#f8fafc';
                ctx.textAlign = 'center';
                
                let label = n.label || n.id;
                if (isMobile && label.length > 14) {
                    label = label.substring(0, 13) + '…';
                }
                ctx.fillText(label, pos.x, pos.y + r + (isMobile ? 10 : 13));
            }
        });
    }

    // Auto re-render on window resize
    window.addEventListener('resize', () => {
        if (currentGraphData && tabGraphContent.style.display !== 'none') {
            requestAnimationFrame(() => renderKnowledgeGraph(currentGraphData));
        }
    });

    // Initial Trigger
    setTimeout(() => {
        handlePrediction();
    }, 150);
});
