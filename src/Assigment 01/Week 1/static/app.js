/**
 * Minimalist Client JS — Diabetes Diagnostic & FPT Long Châu Knowledge Graph
 */

document.addEventListener('DOMContentLoaded', async () => {
    const predictionForm = document.getElementById('predictionForm');
    const submitBtn = document.getElementById('submitBtn');
    const modelSelect = document.getElementById('modelSelect');
    const presetButtons = document.querySelectorAll('.chip-btn');
    
    const singleResultCard = document.getElementById('singleResultCard');
    const comparisonCard = document.getElementById('comparisonCard');
    const resultBadge = document.getElementById('resultBadge');
    
    const statusBanner = document.getElementById('statusBanner');
    const statusHeadline = document.getElementById('statusHeadline');
    const riskProbValue = document.getElementById('riskProbValue');
    const probFill = document.getElementById('probFill');
    const adviceText = document.getElementById('adviceText');
    
    const valRocAuc = document.getElementById('valRocAuc');
    const valAcc = document.getElementById('valAcc');
    const valF1 = document.getElementById('valF1');
    const valRecall = document.getElementById('valRecall');
    
    const avgProb = document.getElementById('avgProb');
    const consensusText = document.getElementById('consensusText');
    const modelBarsContainer = document.getElementById('modelBarsContainer');

    // Long Chau & Knowledge Graph Elements
    const tabProductsBtn = document.getElementById('tabProductsBtn');
    const tabGraphBtn = document.getElementById('tabGraphBtn');
    const tabProductsContent = document.getElementById('tabProductsContent');
    const tabGraphContent = document.getElementById('tabGraphContent');
    const devicesList = document.getElementById('devicesList');
    const supplementsList = document.getElementById('supplementsList');
    const nearestStoreText = document.getElementById('nearestStoreText');
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
            if (tabProductsBtn) tabProductsBtn.click();
        });
    }

    // Bottom Navigation Bar for Mobile App
    const navDiagnoseBtn = document.getElementById('navDiagnoseBtn');
    const navPharmacyBtn = document.getElementById('navPharmacyBtn');
    const longchauSection = document.getElementById('longchauSection');

    function setActiveBottomNav(btn) {
        [navDiagnoseBtn, navPharmacyBtn].forEach(b => b?.classList.remove('active'));
        btn?.classList.add('active');
    }

    if (navDiagnoseBtn) {
        navDiagnoseBtn.addEventListener('click', () => {
            setActiveBottomNav(navDiagnoseBtn);
            document.querySelector('.phone-screen-container')?.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
    if (navPharmacyBtn) {
        navPharmacyBtn.addEventListener('click', () => {
            setActiveBottomNav(navPharmacyBtn);
            if (tabProductsBtn) tabProductsBtn.click();
            longchauSection?.scrollIntoView({ behavior: 'smooth' });
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
        if (data.Pregnancies !== undefined) document.getElementById('pregInput').value = data.Pregnancies;
        if (data.Glucose !== undefined) document.getElementById('glucoseInput').value = data.Glucose;
        if (data.BloodPressure !== undefined) document.getElementById('bpInput').value = data.BloodPressure;
        if (data.SkinThickness !== undefined) document.getElementById('skinInput').value = data.SkinThickness;
        if (data.Insulin !== undefined) document.getElementById('insulinInput').value = data.Insulin;
        if (data.BMI !== undefined) document.getElementById('bmiInput').value = data.BMI;
        if (data.DiabetesPedigreeFunction !== undefined) document.getElementById('dpfInput').value = data.DiabetesPedigreeFunction;
        if (data.Age !== undefined) document.getElementById('ageInput').value = data.Age;
    }

    // 3. Model Switch
    modelSelect.addEventListener('change', () => {
        if (appHeaderModel) {
            appHeaderModel.textContent = modelSelect.value === 'ALL' ? 'So sánh 5 Mô hình AI' : `${modelSelect.value} (Classifier)`;
        }
        handlePrediction();
    });

    // 4. Form Submit
    predictionForm.addEventListener('submit', (e) => {
        e.preventDefault();
        handlePrediction();
    });

    // 5. Tabs Control
    tabProductsBtn.addEventListener('click', () => {
        tabProductsBtn.classList.add('active');
        tabGraphBtn.classList.remove('active');
        tabProductsContent.style.display = 'block';
        tabGraphContent.style.display = 'none';
    });

    tabGraphBtn.addEventListener('click', () => {
        tabGraphBtn.classList.add('active');
        tabProductsBtn.classList.remove('active');
        tabProductsContent.style.display = 'none';
        tabGraphContent.style.display = 'block';
        if (currentGraphData) {
            requestAnimationFrame(() => renderKnowledgeGraph(currentGraphData));
            setTimeout(() => renderKnowledgeGraph(currentGraphData), 50);
            setTimeout(() => renderKnowledgeGraph(currentGraphData), 200);
        }
    });

    function getFormPayload() {
        return {
            Pregnancies: parseFloat(document.getElementById('pregInput').value) || 0,
            Glucose: parseFloat(document.getElementById('glucoseInput').value) || 100,
            BloodPressure: parseFloat(document.getElementById('bpInput').value) || null,
            SkinThickness: parseFloat(document.getElementById('skinInput').value) || null,
            Insulin: parseFloat(document.getElementById('insulinInput').value) || null,
            BMI: parseFloat(document.getElementById('bmiInput').value) || 25.0,
            DiabetesPedigreeFunction: parseFloat(document.getElementById('dpfInput').value) || 0.47,
            Age: parseFloat(document.getElementById('ageInput').value) || 30,
            model_name: modelSelect.value
        };
    }

    // 6. Predict Handler
    async function handlePrediction() {
        const payload = getFormPayload();
        const isAllModels = payload.model_name === 'ALL';

        submitBtn.classList.add('loading');
        submitBtn.querySelector('.btn-text').innerText = 'Đang phân tích...';

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
                    if (data.longchau_care) {
                        renderLongChauCare(data.longchau_care);
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
            submitBtn.querySelector('.btn-text').innerText = 'Chẩn đoán & Phân tích Tri thức';
        }
    }

    // 7. Render Single Result
    function renderSingleModelResult(data) {
        singleResultCard.style.display = 'block';
        comparisonCard.style.display = 'none';

        resultBadge.innerText = data.display_name;
        
        statusBanner.className = `status-banner ${data.status_color}`;
        statusHeadline.innerText = data.status_text;
        riskProbValue.innerText = `Xác suất rủi ro: ${data.diabetic_probability}%`;
        probFill.style.width = `${data.diabetic_probability}%`;
        adviceText.innerText = data.advice;

        const glucoseVal = document.getElementById('glucoseInput').value || 100;
        const bmiVal = document.getElementById('bmiInput').value || 25.0;

        const valIcd = document.getElementById('valIcd');
        const valThreshold = document.getElementById('valThreshold');
        const valGlucoseBio = document.getElementById('valGlucoseBio');
        const valBmiBio = document.getElementById('valBmiBio');

        if (valIcd) valIcd.innerText = data.diabetic_probability >= 25.0 ? 'ICD-10 E11' : 'Bình thường';
        if (valThreshold) valThreshold.innerText = 'θ ≥ 0.25';
        if (valGlucoseBio) valGlucoseBio.innerText = `${glucoseVal} mg/dL`;
        if (valBmiBio) valBmiBio.innerText = `${bmiVal} kg/m²`;
    }

    // 8. Render All Models Comparison
    function renderAllModelsResult(data) {
        singleResultCard.style.display = 'none';
        comparisonCard.style.display = 'block';

        avgProb.innerText = `TB: ${data.summary.average_formatted}`;
        consensusText.innerText = data.summary.consensus;

        const results = data.results;
        modelBarsContainer.innerHTML = '';
        
        results.forEach(item => {
            const prob = item.diabetic_probability;
            const barRow = document.createElement('div');
            barRow.className = `model-bar-item ${item.is_best ? 'best' : ''}`;
            barRow.innerHTML = `
                <div class="bar-row-top">
                    <span>${item.is_best ? '🏆 ' : ''}${item.display_name}</span>
                    <span>${item.prob_formatted}</span>
                </div>
                <div class="bar-row-track">
                    <div class="bar-row-fill" style="width: ${prob}%;"></div>
                </div>
                <div class="bar-row-bottom">
                    <span>${item.prediction === 1 ? '🔴 Dương tính' : '🟢 Âm tính'}</span>
                    <span>ROC-AUC: ${item.roc_auc} | Acc: ${item.accuracy}%</span>
                </div>
            `;
            modelBarsContainer.appendChild(barRow);
        });
    }

    // 9. Render Long Châu Care Products
    function renderLongChauCare(care) {
        // Devices
        devicesList.innerHTML = '';
        if (care.devices && care.devices.length > 0) {
            care.devices.forEach(d => {
                const card = document.createElement('div');
                card.className = 'product-card';
                card.innerHTML = `
                    <div class="p-left">
                        <span class="p-tag">${d.tag}</span>
                        <a href="${d.url}" target="_blank" class="p-name">${d.name}</a>
                        <span class="p-benefit">${d.benefit}</span>
                    </div>
                    <div class="p-right">
                        <div class="p-price">${d.price_formatted}</div>
                        <a href="${d.url}" target="_blank" class="p-buy-btn">Mua tại Long Châu ➔</a>
                    </div>
                `;
                devicesList.appendChild(card);
            });
        } else {
            devicesList.innerHTML = '<p style="font-size:0.8rem; color:#64748b;">Chỉ số tốt, không yêu cầu thiết bị chuyên sâu.</p>';
        }

        // Supplements
        supplementsList.innerHTML = '';
        if (care.supplements && care.supplements.length > 0) {
            care.supplements.forEach(s => {
                const card = document.createElement('div');
                card.className = 'product-card';
                card.innerHTML = `
                    <div class="p-left">
                        <span class="p-tag">${s.tag}</span>
                        <a href="${s.url}" target="_blank" class="p-name">${s.name}</a>
                        <span class="p-benefit">${s.benefit}</span>
                    </div>
                    <div class="p-right">
                        <div class="p-price">${s.price_formatted}</div>
                        <a href="${s.url}" target="_blank" class="p-buy-btn">Mua tại Long Châu ➔</a>
                    </div>
                `;
                supplementsList.appendChild(card);
            });
        }

        // Store
        if (care.store) {
            nearestStoreText.innerText = `${care.store.name} (Hotline: ${care.store.hotline})`;
        }
    }

    // 10. Knowledge Graph 2D Canvas Renderer (Normalized Proportional Coordinates)
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

        let devIndex = 0;
        let suppIndex = 0;

        nodes.forEach((n) => {
            let rx = 0.5, ry = 0.5;
            if (n.id === 'patient') {
                rx = 0.16; ry = 0.50;
            } else if (n.id === 'bio_glucose') {
                rx = 0.16; ry = 0.16;
            } else if (n.id === 'bio_bmi') {
                rx = 0.16; ry = 0.84;
            } else if (n.id === 'prediction') {
                rx = 0.42; ry = 0.35;
            } else if (n.id === 'store_01') {
                rx = 0.42; ry = 0.78;
            } else if (n.id === 'disease') {
                rx = 0.68; ry = 0.35;
            } else if (n.group === 'device') {
                rx = 0.88;
                ry = 0.18 + devIndex * 0.22;
                devIndex++;
            } else if (n.group === 'supplement') {
                rx = 0.88;
                ry = 0.64 + suppIndex * 0.22;
                suppIndex++;
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
    setTimeout(async () => {
        await handlePrediction();
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('tab') === 'graph') {
            tabGraphBtn.click();
        }
    }, 150);
});
