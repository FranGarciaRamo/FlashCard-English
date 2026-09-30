<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <title>Flashcards - Swiss Re Business English</title>

  <!-- Configuración PWA e iOS -->
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <meta name="apple-mobile-web-app-title" content="Flashcards" />
  <meta name="theme-color" content="#121212" />

  <style>
    :root {
      --bg: #121212;
      --card-front: #242424;
      --card-back: #22252a;
      --border-color: #2f2f2f;
      --star-color: #ffd700;
      --text-main: #f0f0f0;
      --text-dim: #888888;
      --btn-bg: #1e1e1e;
      --btn-active: #303030;
      --success: #4caf50;
      --danger: #ff5252;
    }

    * {
      box-sizing: border-box;
      user-select: none;
      -webkit-user-select: none;
      -webkit-tap-highlight-color: transparent;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      min-height: 100vh;
      min-height: -webkit-fill-available;
      display: flex;
      flex-direction: column;
      padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);
      overflow: hidden;
    }

    .app-container {
      flex: 1;
      display: flex;
      flex-direction: column;
      max-width: 580px;
      width: 100%;
      margin: 0 auto;
      padding: 16px 20px 24px 20px;
      height: 100%;
    }

    /* Contenedor de la Tarjeta */
    .card-stage {
      flex: 1;
      position: relative;
      perspective: 1000px;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 320px;
    }

    .card-placeholder {
      position: absolute;
      width: 100%;
      height: 100%;
      background: #1c1c1c;
      border: 1px solid #282828;
      border-radius: 24px;
      transform: translateY(8px) scale(0.97);
      opacity: 0.6;
      z-index: 1;
    }

    .card {
      position: relative;
      width: 100%;
      height: 100%;
      border-radius: 24px;
      border: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 32px 24px;
      text-align: center;
      cursor: pointer;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.45);
      transition: background-color 0.25s ease, border-color 0.25s ease;
      z-index: 2;
    }

    .card.front {
      background-color: var(--card-front);
    }

    .card.back {
      background-color: var(--card-back);
    }

    /* Animación de caída idéntica a Python (64px y fade out) */
    .card.anim-fall {
      transform: translateY(64px);
      opacity: 0;
      transition: transform 0.16s cubic-bezier(0.2, 0, 0.4, 1), opacity 0.16s ease-out;
    }

    .card-star-badge {
      position: absolute;
      top: 20px;
      right: 22px;
      font-size: 20px;
      color: var(--star-color);
      display: none;
    }

    .card-star-badge.active {
      display: block;
    }

    .card-text {
      font-size: 24px;
      font-weight: 600;
      line-height: 1.4;
      word-break: break-word;
    }

    .card.back .card-text {
      font-weight: 400;
      font-size: 21px;
    }

    .deck-finished {
      color: var(--success);
      font-size: 19px;
      font-weight: 600;
      line-height: 1.6;
      text-align: center;
    }

    /* Controles inferiores */
    .controls {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 18px;
      gap: 8px;
    }

    .btn-group {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .icon-btn {
      background-color: var(--btn-bg);
      color: #dddddd;
      border: none;
      outline: none;
      border-radius: 12px;
      height: 44px;
      min-width: 44px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 17px;
      cursor: pointer;
      transition: background 0.15s, transform 0.1s;
    }

    .icon-btn:active {
      background-color: var(--btn-active);
      transform: scale(0.96);
    }

    .icon-btn:disabled {
      opacity: 0.35;
      cursor: default;
    }

    .btn-action {
      min-width: 58px;
      height: 48px;
      font-size: 20px;
      background: #202020;
    }

    .btn-fav.active {
      color: var(--star-color);
    }

    .stats-info {
      font-size: 13px;
      color: var(--text-dim);
      white-space: nowrap;
      margin-left: 2px;
    }

    /* Modal / Menús */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(4px);
      -webkit-backdrop-filter: blur(4px);
      z-index: 100;
      display: flex;
      align-items: flex-end;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s ease;
    }

    .modal-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }

    .sheet-modal {
      background: #181818;
      border-radius: 24px 24px 0 0;
      width: 100%;
      max-height: 85vh;
      display: flex;
      flex-direction: column;
      transform: translateY(100%);
      transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
      padding: 16px 18px calc(env(safe-area-inset-bottom) + 16px) 18px;
    }

    .modal-overlay.open .sheet-modal {
      transform: translateY(0);
    }

    .sheet-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }

    .sheet-title {
      font-size: 17px;
      font-weight: 600;
    }

    .action-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 6px;
    }

    .action-btn {
      background: #222222;
      border: none;
      padding: 14px 16px;
      border-radius: 12px;
      color: #fff;
      font-size: 15px;
      text-align: left;
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
    }

    .action-btn:active {
      background: #2c2c2c;
    }

    /* Buscador y Gestor de Tarjetas */
    .search-bar {
      display: flex;
      gap: 8px;
      margin: 10px 0 14px 0;
    }

    .search-input {
      flex: 1;
      background: #262626;
      border: none;
      border-radius: 10px;
      padding: 10px 14px;
      font-size: 15px;
      color: #fff;
      outline: none;
    }

    .list-container {
      flex: 1;
      overflow-y: auto;
      max-height: 48vh;
      border-radius: 12px;
      background: #141414;
      border: 1px solid #242424;
    }

    .list-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 14px;
      border-bottom: 1px solid #1f1f1f;
      gap: 10px;
    }

    .list-item-content {
      flex: 1;
    }

    .list-en {
      font-size: 15px;
      font-weight: 500;
    }

    .list-es {
      font-size: 13px;
      color: #999;
      margin-top: 2px;
    }

    .list-actions {
      display: flex;
      gap: 8px;
    }

    .btn-tiny {
      background: #222;
      border: none;
      color: #aaa;
      border-radius: 8px;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }

    .btn-tiny.fav-active {
      color: var(--star-color);
    }

    .btn-tiny.del-btn {
      color: var(--danger);
    }
  </style>
</head>
<body>
  <div class="app-container">
    <!-- Tarjeta Principal -->
    <div class="card-stage">
      <div class="card-placeholder"></div>
      <div class="card front" id="cardElement" onclick="flipCard()">
        <span class="card-star-badge" id="cardStarBadge">★</span>
        <div class="card-text" id="cardText">Cargando...</div>
      </div>
    </div>

    <!-- Barra de Controles -->
    <div class="controls">
      <div class="btn-group">
        <button class="icon-btn" id="btnPrev" onclick="previousCard()" aria-label="Tarjeta anterior">←</button>
        <span class="stats-info" id="statsDisplay">0 de 0</span>
      </div>

      <div class="btn-group">
        <button class="icon-btn btn-action" onclick="markWrong()" aria-label="Marcar incorrecto">✕</button>
        <button class="icon-btn btn-action" onclick="markCorrect()" aria-label="Marcar correcto">✓</button>
      </div>

      <div class="btn-group">
        <button class="icon-btn btn-fav" id="btnFav" onclick="toggleFavorite()" aria-label="Marcar favorita">☆</button>
        <button class="icon-btn" onclick="speakCard()" aria-label="Pronunciación">🔊</button>
        <button class="icon-btn" onclick="openMenu()" aria-label="Menú">⋯</button>
      </div>
    </div>
  </div>

  <!-- Modal Menú de Opciones -->
  <div class="modal-overlay" id="menuModal" onclick="closeModals(event)">
    <div class="sheet-modal">
      <div class="sheet-header">
        <div class="sheet-title">Opciones de estudio</div>
        <button class="icon-btn" style="height:32px; min-width:32px;" onclick="closeModals()">✕</button>
      </div>
      <div class="action-list">
        <button class="action-btn" onclick="resetDeck(onlyFavorites)">🔄 Reiniciar mazo actual</button>
        <button class="action-btn" id="btnToggleMode" onclick="toggleMode()">⭐ Estudiar solo favoritas</button>
        <button class="action-btn" onclick="openManager()">✏️ Gestionar tarjetas (Buscar / Añadir)</button>
      </div>
    </div>
  </div>

  <!-- Modal Gestor de Tarjetas -->
  <div class="modal-overlay" id="managerModal" onclick="closeModals(event)">
    <div class="sheet-modal" style="max-height: 88vh;">
      <div class="sheet-header">
        <div class="sheet-title">Gestión de Tarjetas</div>
        <button class="icon-btn" style="height:32px; min-width:32px;" onclick="closeModals()">✕</button>
      </div>
      
      <div class="search-bar">
        <input type="text" id="searchInput" class="search-input" placeholder="🔍 Buscar término..." oninput="renderManagerList()" />
        <button class="icon-btn" style="font-size: 14px; padding: 0 12px; width:auto;" onclick="addNewCard()">➕ Nueva</button>
      </div>

      <div class="list-container" id="cardsListContainer">
        <!-- Renderizado dinámico -->
      </div>
    </div>
  </div>

  <script>
    // Conjunto de datos base idéntico a flashcards.py
    const INITIAL_DATA = [
      {"en": "Financial accounting", "es": "Contabilidad financiera", "favorite": false},
      {"en": "Management accounting", "es": "Contabilidad de gestión", "favorite": false},
      {"en": "Financial statements", "es": "Estados financieros", "favorite": false},
      {"en": "Balance sheet", "es": "Balance de situación", "favorite": false},
      {"en": "Income statement", "es": "Cuenta de resultados", "favorite": false},
      {"en": "Cash flow statement", "es": "Estado de flujos de efectivo", "favorite": false},
      {"en": "Statement of equity", "es": "Estado de cambios en el patrimonio neto", "favorite": false},
      {"en": "Assets", "es": "Activos", "favorite": false},
      {"en": "Liabilities", "es": "Pasivos", "favorite": false},
      {"en": "Equity", "es": "Patrimonio neto", "favorite": false},
      {"en": "Current assets", "es": "Activos corrientes", "favorite": false},
      {"en": "Non-current assets", "es": "Activos no corrientes", "favorite": false},
      {"en": "Current liabilities", "es": "Pasivos corrientes", "favorite": false},
      {"en": "Non-current liabilities", "es": "Pasivos no corrientes", "favorite": false},
      {"en": "Shareholders' equity", "es": "Patrimonio neto de los accionistas", "favorite": false},
      {"en": "Book value", "es": "Valor contable", "favorite": false},
      {"en": "Carrying amount", "es": "Importe en libros", "favorite": false},
      {"en": "Revenue", "es": "Ingresos", "favorite": false},
      {"en": "Sales", "es": "Ventas", "favorite": false},
      {"en": "Cost of sales", "es": "Coste de ventas", "favorite": false},
      {"en": "Cost of goods sold", "es": "Coste de los bienes vendidos", "favorite": false},
      {"en": "Operating expenses", "es": "Gastos operativos", "favorite": false},
      {"en": "Net profit", "es": "Beneficio neto", "favorite": false},
      {"en": "Net loss", "es": "Pérdida neta", "favorite": false},
      {"en": "Operating profit", "es": "Beneficio operativo", "favorite": false},
      {"en": "Gross profit", "es": "Beneficio bruto", "favorite": false},
      {"en": "Profit before tax", "es": "Beneficio antes de impuestos", "favorite": false},
      {"en": "Profit after tax", "es": "Beneficio después de impuestos", "favorite": false},
      {"en": "Earnings", "es": "Beneficios / ganancias", "favorite": false},
      {"en": "Loss", "es": "Pérdida / siniestro", "favorite": false},
      {"en": "Profitability", "es": "Rentabilidad", "favorite": false},
      {"en": "Margin", "es": "Margen", "favorite": false},
      {"en": "Gross margin", "es": "Margen bruto", "favorite": false},
      {"en": "Operating margin", "es": "Margen operativo", "favorite": false},
      {"en": "Net profit margin", "es": "Margen de beneficio neto", "favorite": false},
      {"en": "Financial analysis", "es": "Análisis financiero", "favorite": false},
      {"en": "Financial performance", "es": "Rendimiento / desempeño financiero", "favorite": false},
      {"en": "Financial position", "es": "Situación financiera", "favorite": false},
      {"en": "Key performance indicator (KPI)", "es": "Indicador clave de rendimiento", "favorite": false},
      {"en": "Financial ratio", "es": "Ratio financiero", "favorite": false},
      {"en": "Liquidity", "es": "Liquidez", "favorite": false},
      {"en": "Solvency", "es": "Solvencia", "favorite": false},
      {"en": "Leverage", "es": "Apalancamiento", "favorite": false},
      {"en": "Debt", "es": "Deuda", "favorite": false},
      {"en": "Debt-to-equity ratio", "es": "Ratio de deuda sobre patrimonio neto", "favorite": false},
      {"en": "Return on equity (ROE)", "es": "Rentabilidad sobre recursos propios", "favorite": false},
      {"en": "Return on assets (ROA)", "es": "Rentabilidad sobre activos", "favorite": false},
      {"en": "Working capital", "es": "Capital circulante / fondo de maniobra", "favorite": false},
      {"en": "Cash flow", "es": "Flujo de caja", "favorite": false},
      {"en": "Free cash flow", "es": "Flujo de caja libre", "favorite": false},
      {"en": "Cash inflow", "es": "Entrada de efectivo", "favorite": false},
      {"en": "Cash outflow", "es": "Salida de efectivo", "favorite": false},
      {"en": "Trend", "es": "Tendencia", "favorite": false},
      {"en": "Growth", "es": "Crecimiento", "favorite": false},
      {"en": "Decline", "es": "Descenso", "favorite": false},
      {"en": "Increase", "es": "Aumento", "favorite": false},
      {"en": "Decrease", "es": "Disminución", "favorite": false},
      {"en": "Key driver", "es": "Factor principal / impulsor", "favorite": false},
      {"en": "Main contributor", "es": "Principal contribuyente", "favorite": false},
      {"en": "Underlying performance", "es": "Rendimiento subyacente", "favorite": false},
      {"en": "Financial reporting", "es": "Reporting / información financiera", "favorite": false},
      {"en": "Management reporting", "es": "Reporting para la dirección", "favorite": false},
      {"en": "External reporting", "es": "Reporting externo", "favorite": false},
      {"en": "Internal reporting", "es": "Reporting interno", "favorite": false},
      {"en": "Quarterly reporting", "es": "Reporting trimestral", "favorite": false},
      {"en": "Annual reporting", "es": "Reporting anual", "favorite": false},
      {"en": "Financial disclosure", "es": "Información financiera divulgada", "favorite": false},
      {"en": "Reporting period", "es": "Periodo de reporting", "favorite": false},
      {"en": "Reporting package", "es": "Paquete de reporting", "favorite": false},
      {"en": "Financial data", "es": "Datos financieros", "favorite": false},
      {"en": "Financial information", "es": "Información financiera", "favorite": false},
      {"en": "Actuals", "es": "Datos reales / resultados reales", "favorite": false},
      {"en": "Forecast", "es": "Previsión", "favorite": false},
      {"en": "Budget", "es": "Presupuesto", "favorite": false},
      {"en": "Budget vs. actuals", "es": "Presupuesto frente a resultados reales", "favorite": false},
      {"en": "Variance", "es": "Desviación", "favorite": false},
      {"en": "Variance analysis", "es": "Análisis de desviaciones", "favorite": false},
      {"en": "Favourable variance", "es": "Desviación favorable", "favorite": false},
      {"en": "Unfavourable variance", "es": "Desviación desfavorable", "favorite": false},
      {"en": "To report", "es": "Informar / reportar", "favorite": false},
      {"en": "To consolidate", "es": "Consolidar", "favorite": false},
      {"en": "To reconcile", "es": "Conciliar", "favorite": false},
      {"en": "Reconciliation", "es": "Conciliación", "favorite": false},
      {"en": "To analyse", "es": "Analizar", "favorite": false},
      {"en": "To interpret", "es": "Interpretar", "favorite": false},
      {"en": "To monitor", "es": "Supervisar / hacer seguimiento", "favorite": false},
      {"en": "To track", "es": "Hacer seguimiento de", "favorite": false},
      {"en": "To review", "es": "Revisar", "favorite": false},
      {"en": "To identify", "es": "Identificar", "favorite": false},
      {"en": "To investigate", "es": "Investigar / analizar", "favorite": false},
      {"en": "To assess", "es": "Evaluar", "favorite": false},
      {"en": "To compare", "es": "Comparar", "favorite": false},
      {"en": "Compared with", "es": "Comparado con", "favorite": false},
      {"en": "Compared to", "es": "Comparado con", "favorite": false},
      {"en": "Year-on-year (YoY)", "es": "Interanual", "favorite": false},
      {"en": "Quarter-on-quarter (QoQ)", "es": "Trimestral / respecto al trimestre anterior", "favorite": false},
      {"en": "Month-on-month (MoM)", "es": "Mensual / respecto al mes anterior", "favorite": false},
      {"en": "IFRS", "es": "Normas Internacionales de Información Financiera", "favorite": false},
      {"en": "IFRS standards", "es": "Normas IFRS", "favorite": false},
      {"en": "Accounting standard", "es": "Norma contable", "favorite": false},
      {"en": "Generally Accepted Accounting Principles (GAAP)", "es": "Principios contables generalmente aceptados", "favorite": false},
      {"en": "Spanish GAAP", "es": "Normativa contable española", "favorite": false},
      {"en": "Recognition", "es": "Reconocimiento contable", "favorite": false},
      {"en": "Measurement", "es": "Valoración / medición contable", "favorite": false},
      {"en": "Fair value", "es": "Valor razonable", "favorite": false},
      {"en": "Historical cost", "es": "Coste histórico", "favorite": false},
      {"en": "Accrual", "es": "Devengo", "favorite": false},
      {"en": "Accrual accounting", "es": "Contabilidad por devengo", "favorite": false},
      {"en": "Provision", "es": "Provisión", "favorite": false},
      {"en": "Impairment", "es": "Deterioro de valor", "favorite": false},
      {"en": "Depreciation", "es": "Depreciación / amortización de activos materiales", "favorite": false},
      {"en": "Amortisation", "es": "Amortización de activos intangibles", "favorite": false},
      {"en": "Useful life", "es": "Vida útil", "favorite": false},
      {"en": "Asset recognition", "es": "Reconocimiento de un activo", "favorite": false},
      {"en": "Liability recognition", "es": "Reconocimiento de un pasivo", "favorite": false},
      {"en": "Consolidation", "es": "Consolidación", "favorite": false},
      {"en": "Consolidated financial statements", "es": "Estados financieros consolidados", "favorite": false},
      {"en": "Subsidiary", "es": "Filial", "favorite": false},
      {"en": "Parent company", "es": "Sociedad dominante / matriz", "favorite": false},
      {"en": "Accounting treatment", "es": "Tratamiento contable", "favorite": false},
      {"en": "Accounting policy", "es": "Política contable", "favorite": false},
      {"en": "Internal controls", "es": "Controles internos", "favorite": false},
      {"en": "Audit", "es": "Auditoría", "favorite": false},
      {"en": "Auditor", "es": "Auditor", "favorite": false},
      {"en": "Audit trail", "es": "Pista de auditoría / trazabilidad", "favorite": false},
      {"en": "Insurance", "es": "Seguro", "favorite": false},
      {"en": "Reinsurance", "es": "Reaseguro", "favorite": false},
      {"en": "Insurer", "es": "Aseguradora", "favorite": false},
      {"en": "Reinsurer", "es": "Reaseguradora", "favorite": false},
      {"en": "Policy", "es": "Póliza", "favorite": false},
      {"en": "Policyholder", "es": "Tomador del seguro", "favorite": false},
      {"en": "Insured", "es": "Asegurado", "favorite": false},
      {"en": "Premium", "es": "Prima", "favorite": false},
      {"en": "Insurance premium", "es": "Prima de seguro", "favorite": false},
      {"en": "Claim", "es": "Siniestro / reclamación", "favorite": false},
      {"en": "Claims", "es": "Siniestros", "favorite": false},
      {"en": "Underwriting", "es": "Suscripción de riesgos", "favorite": false},
      {"en": "Underwriter", "es": "Suscriptor / analista de riesgos", "favorite": false},
      {"en": "Risk", "es": "Riesgo", "favorite": false},
      {"en": "Risk management", "es": "Gestión de riesgos", "favorite": false},
      {"en": "Reserve", "es": "Reserva / provisión", "favorite": false},
      {"en": "Insurance reserve", "es": "Reserva de seguros", "favorite": false},
      {"en": "Cedant", "es": "Cedente", "favorite": false},
      {"en": "Ceded business", "es": "Negocio cedido", "favorite": false},
      {"en": "Life insurance", "es": "Seguro de vida", "favorite": false},
      {"en": "Health insurance", "es": "Seguro de salud", "favorite": false},
      {"en": "Life & Health (L&H)", "es": "Vida y Salud", "favorite": false},
      {"en": "Property & Casualty (P&C)", "es": "Daños y Responsabilidad Civil", "favorite": false},
      {"en": "Reinsurance contract", "es": "Contrato de reaseguro", "favorite": false},
      {"en": "Reinsurance premium", "es": "Prima de reaseguro", "favorite": false},
      {"en": "Reinsurance claim", "es": "Siniestro de reaseguro", "favorite": false},
      {"en": "Risk exposure", "es": "Exposición al riesgo", "favorite": false},
      {"en": "Portfolio", "es": "Cartera", "favorite": false},
      {"en": "Underwriting result", "es": "Resultado de suscripción", "favorite": false},
      {"en": "Shareholder", "es": "Accionista", "favorite": false},
      {"en": "Stakeholder", "es": "Parte interesada", "favorite": false},
      {"en": "Board of directors", "es": "Consejo de administración", "favorite": false},
      {"en": "Chairperson", "es": "Presidente/a", "favorite": false},
      {"en": "Chief Executive Officer (CEO)", "es": "Director ejecutivo / consejero delegado", "favorite": false},
      {"en": "Chief Financial Officer (CFO)", "es": "Director financiero", "favorite": false},
      {"en": "Headquarters", "es": "Sede central", "favorite": false},
      {"en": "Branch", "es": "Sucursal", "favorite": false},
      {"en": "Department", "es": "Departamento", "favorite": false},
      {"en": "Division", "es": "División", "favorite": false},
      {"en": "Management", "es": "Dirección / gestión", "favorite": false},
      {"en": "Senior management", "es": "Alta dirección", "favorite": false},
      {"en": "Workforce", "es": "Plantilla / fuerza laboral", "favorite": false},
      {"en": "Employee", "es": "Empleado", "favorite": false},
      {"en": "Employer", "es": "Empleador", "favorite": false},
      {"en": "Colleague", "es": "Compañero de trabajo", "favorite": false},
      {"en": "Ownership", "es": "Propiedad / participación", "favorite": false},
      {"en": "To own", "es": "Poseer / ser propietario de", "favorite": false},
      {"en": "Merger", "es": "Fusión", "favorite": false},
      {"en": "Acquisition", "es": "Adquisición", "favorite": false},
      {"en": "Takeover", "es": "Adquisición / toma de control", "favorite": false},
      {"en": "Joint venture", "es": "Empresa conjunta", "favorite": false},
      {"en": "Bankruptcy", "es": "Quiebra / bancarrota", "favorite": false},
      {"en": "Creditor", "es": "Acreedor", "favorite": false},
      {"en": "Debtor", "es": "Deudor", "favorite": false},
      {"en": "Loan", "es": "Préstamo", "favorite": false},
      {"en": "Interest rate", "es": "Tipo de interés", "favorite": false},
      {"en": "Dividend", "es": "Dividendo", "favorite": false},
      {"en": "Share", "es": "Acción / participación", "favorite": false},
      {"en": "To achieve", "es": "Lograr / alcanzar", "favorite": false},
      {"en": "To calculate", "es": "Calcular", "favorite": false},
      {"en": "To coordinate", "es": "Coordinar", "favorite": false},
      {"en": "To improve", "es": "Mejorar", "favorite": false},
      {"en": "To increase", "es": "Aumentar", "favorite": false},
      {"en": "To decrease", "es": "Disminuir", "favorite": false},
      {"en": "To manage", "es": "Gestionar", "favorite": false},
      {"en": "To maintain", "es": "Mantener", "favorite": false},
      {"en": "To prepare", "es": "Preparar", "favorite": false},
      {"en": "To provide", "es": "Proporcionar", "favorite": false},
      {"en": "To support", "es": "Apoyar", "favorite": false},
      {"en": "To contribute", "es": "Contribuir", "favorite": false},
      {"en": "To streamline", "es": "Optimizar / simplificar", "favorite": false},
      {"en": "To automate", "es": "Automatizar", "favorite": false},
      {"en": "To forecast", "es": "Prever / realizar previsiones", "favorite": false},
      {"en": "To allocate", "es": "Asignar", "favorite": false},
      {"en": "To handle", "es": "Gestionar / encargarse de", "favorite": false},
      {"en": "Driven by", "es": "Impulsado por", "favorite": false},
      {"en": "Mainly driven by", "es": "Principalmente impulsado por", "favorite": false},
      {"en": "Due to", "es": "Debido a", "favorite": false},
      {"en": "As a result of", "es": "Como resultado de", "favorite": false},
      {"en": "Compared with the previous quarter", "es": "Comparado con el trimestre anterior", "favorite": false},
      {"en": "Compared with the previous year", "es": "Comparado con el año anterior", "favorite": false},
      {"en": "In line with", "es": "En línea con", "favorite": false},
      {"en": "Above expectations", "es": "Por encima de las expectativas", "favorite": false},
      {"en": "Below expectations", "es": "Por debajo de las expectativas", "favorite": false},
      {"en": "Higher than expected", "es": "Superior a lo esperado", "favorite": false},
      {"en": "Lower than expected", "es": "Inferior a lo esperado", "favorite": false},
      {"en": "The main driver was", "es": "El principal factor fue", "favorite": false},
      {"en": "The main contributor was", "es": "El principal contribuyente fue", "favorite": false},
      {"en": "There was an increase in", "es": "Hubo un aumento de", "favorite": false},
      {"en": "There was a decrease in", "es": "Hubo una disminución de", "favorite": false},
      {"en": "This was mainly due to", "es": "Esto se debió principalmente a", "favorite": false},
      {"en": "We identified a variance", "es": "Identificamos una desviación", "favorite": false},
      {"en": "We need to investigate the variance", "es": "Tenemos que analizar la desviación", "favorite": false},
      {"en": "The results are in line with the forecast", "es": "Los resultados están en línea con la previsión", "favorite": false},
      {"en": "The figures show", "es": "Las cifras muestran", "favorite": false},
      {"en": "Based on the available data", "es": "Basándonos en los datos disponibles", "favorite": false},
      {"en": "From a financial perspective", "es": "Desde una perspectiva financiera", "favorite": false},
      {"en": "In terms of profitability", "es": "En términos de rentabilidad", "favorite": false},
      {"en": "From a reporting perspective", "es": "Desde una perspectiva de reporting", "favorite": false},
      {"en": "Shopkeepers", "es": "Comerciantes / tenderos", "favorite": false},
      {"en": "Retailers", "es": "Minoristas", "favorite": false},
      {"en": "Profit-seeking", "es": "Búsqueda de beneficios", "favorite": false},
      {"en": "Profits", "es": "Beneficios", "favorite": false},
      {"en": "Revenues", "es": "Ingresos", "favorite": false},
      {"en": "To supply", "es": "Suministrar", "favorite": false},
      {"en": "To form", "es": "Formar", "favorite": false},
      {"en": "Wholesalers", "es": "Mayoristas", "favorite": false},
      {"en": "To make a loss", "es": "Tener pérdidas", "favorite": false},
      {"en": "Gaining profits", "es": "Tener beneficios", "favorite": false},
      {"en": "Buyer", "es": "Comprador", "favorite": false},
      {"en": "Seller", "es": "Vendedor", "favorite": false},
      {"en": "Expenses", "es": "Gastos", "favorite": false},
      {"en": "To fail", "es": "Fracasar", "favorite": false},
      {"en": "To succeed", "es": "Tener éxito", "favorite": false},
      {"en": "Investors", "es": "Inversores", "favorite": false},
      {"en": "Wealth", "es": "Riqueza", "favorite": false},
      {"en": "Take the risk", "es": "Correr riesgos", "favorite": false},
      {"en": "Standard of living", "es": "Nivel de vida", "favorite": false},
      {"en": "Customers", "es": "Clientes", "favorite": false},
      {"en": "Divisions", "es": "Divisiones", "favorite": false},
      {"en": "Hierarchy", "es": "Jerarquía", "favorite": false},
      {"en": "Chief", "es": "Jefe", "favorite": false},
      {"en": "Account", "es": "Cuenta", "favorite": false},
      {"en": "Accounting", "es": "Contabilidad", "favorite": false},
      {"en": "Accountants", "es": "Contables", "favorite": false},
      {"en": "Concerned", "es": "Preocupado", "favorite": false},
      {"en": "Purchasing", "es": "Compras / adquisición", "favorite": false},
      {"en": "Supplies", "es": "Suministros", "favorite": false},
      {"en": "Wages", "es": "Salarios / sueldos", "favorite": false},
      {"en": "Welfare", "es": "Bienestar", "favorite": false},
      {"en": "Liaison", "es": "Enlace", "favorite": false},
      {"en": "Dismissal", "es": "Despido", "favorite": false},
      {"en": "Loans", "es": "Préstamos", "favorite": false},
      {"en": "Below", "es": "Debajo", "favorite": false},
      {"en": "Debts", "es": "Deudas", "favorite": false},
      {"en": "Franchising", "es": "Franquicia", "favorite": false},
      {"en": "Franchiser", "es": "Franquiciador", "favorite": false},
      {"en": "Franchisee", "es": "Franquiciado", "favorite": false},
      {"en": "Subsidiaries", "es": "Filiales", "favorite": false},
      {"en": "Bankrupt", "es": "En bancarrota", "favorite": false},
      {"en": "Sole trader", "es": "Autónomo", "favorite": false},
      {"en": "Launch", "es": "Lanzar", "favorite": false},
      {"en": "Achieve sales", "es": "Lograr / alcanzar ventas", "favorite": false},
      {"en": "Retail outlet", "es": "Punto de venta", "favorite": false},
      {"en": "Purchaser", "es": "Comprador", "favorite": false},
      {"en": "Cash", "es": "Efectivo", "favorite": false},
      {"en": "Leadership", "es": "Liderazgo", "favorite": false},
      {"en": "Throughout", "es": "En todo / a través de", "favorite": false},
      {"en": "Branches", "es": "Sucursales", "favorite": false},
      {"en": "Trading documents", "es": "Documentos comerciales", "favorite": false},
      {"en": "Supplementary documents", "es": "Documentos complementarios", "favorite": false},
      {"en": "Country agreements", "es": "Acuerdos internacionales", "favorite": false},
      {"en": "Purchase order", "es": "Orden de compra", "favorite": false},
      {"en": "Invoice", "es": "Factura", "favorite": false},
      {"en": "Statement", "es": "Declaración / estado de cuenta", "favorite": false},
      {"en": "Enquiry", "es": "Consulta / solicitud de información", "favorite": false},
      {"en": "Quotation", "es": "Cotización", "favorite": false},
      {"en": "Consignment note", "es": "Carta de porte", "favorite": false},
      {"en": "Air waybill", "es": "Carta de porte aéreo", "favorite": false},
      {"en": "Bill of lading", "es": "Guía de carga / conocimiento de embarque", "favorite": false},
      {"en": "Acknowledgement", "es": "Reconocimiento", "favorite": false},
      {"en": "Delivery note", "es": "Albarán", "favorite": false},
      {"en": "Draft", "es": "Letra de cambio / borrador", "favorite": false},
      {"en": "Prepayment", "es": "Pago anticipado", "favorite": false},
      {"en": "Bill of Exchange", "es": "Letra de cambio", "favorite": false},
      {"en": "Discount", "es": "Descuento", "favorite": false},
      {"en": "Terms", "es": "Términos", "favorite": false},
      {"en": "Guarantee", "es": "Garantía", "favorite": false},
      {"en": "Size", "es": "Tamaño", "favorite": false},
      {"en": "Reach", "es": "Llegar a", "favorite": false},
      {"en": "Consign", "es": "Enviar", "favorite": false},
      {"en": "Consignee", "es": "Destinatario", "favorite": false},
      {"en": "Consignor", "es": "Remitente", "favorite": false},
      {"en": "Recruitment", "es": "Reclutamiento", "favorite": false},
      {"en": "Covering letter", "es": "Carta de presentación", "favorite": false},
      {"en": "Applicants", "es": "Candidatos / solicitantes", "favorite": false},
      {"en": "Shortlist", "es": "Lista de preseleccionados", "favorite": false},
      {"en": "To attend an interview", "es": "Asistir a una entrevista", "favorite": false},
      {"en": "To hire", "es": "Contratar", "favorite": false},
      {"en": "Probationary period", "es": "Periodo de prueba", "favorite": false},
      {"en": "Application form", "es": "Formulario de solicitud", "favorite": false},
      {"en": "Psychometric test", "es": "Test psicométrico", "favorite": false},
      {"en": "To qualify", "es": "Cumplir los requisitos / calificar", "favorite": false},
      {"en": "To be qualified", "es": "Estar cualificado", "favorite": false},
      {"en": "Degree", "es": "Carrera / título universitario", "favorite": false},
      {"en": "Internship / Work placement", "es": "Prácticas en empresa", "favorite": false},
      {"en": "Appoint", "es": "Nombrar / designar", "favorite": false},
      {"en": "Appointment", "es": "Nombramiento / cita", "favorite": false},
      {"en": "Dismiss", "es": "Despedir", "favorite": false},
      {"en": "Fire", "es": "Despedir", "favorite": false},
      {"en": "Sack", "es": "Despedir", "favorite": false},
      {"en": "Resign", "es": "Dimitir / renunciar", "favorite": false},
      {"en": "Fill jobs", "es": "Cubrir puestos", "favorite": false},
      {"en": "Fields", "es": "Áreas / campos", "favorite": false},
      {"en": "Budget analysts", "es": "Analistas del presupuesto", "favorite": false},
      {"en": "Arrange", "es": "Organizar", "favorite": false},
      {"en": "Lead", "es": "Dirigir", "favorite": false},
      {"en": "Beliefs", "es": "Creencias", "favorite": false},
      {"en": "Fellowships", "es": "Becas / agrupaciones", "favorite": false},
      {"en": "Knowledge", "es": "Conocimiento", "favorite": false},
      {"en": "Bureaucracy", "es": "Burocracia", "favorite": false},
      {"en": "Deal", "es": "Acuerdo / oferta", "favorite": false},
      {"en": "Relationships", "es": "Relaciones", "favorite": false},
      {"en": "Exchanging business cards", "es": "Intercambio de tarjetas de visita", "favorite": false},
      {"en": "Shaking hands", "es": "Estrechar la mano", "favorite": false},
      {"en": "Kissing", "es": "Besar", "favorite": false},
      {"en": "Bowing", "es": "Inclinación", "favorite": false},
      {"en": "Lend", "es": "Prestar", "favorite": false},
      {"en": "Borrow", "es": "Pedir prestado", "favorite": false},
      {"en": "Consignment", "es": "Envío / consignación", "favorite": false},
      {"en": "To hang on", "es": "Estar a la espera (teléfono)", "favorite": false},
      {"en": "To leave a message", "es": "Dejar un mensaje", "favorite": false},
      {"en": "To hang up", "es": "Colgar", "favorite": false},
      {"en": "To call back", "es": "Devolver la llamada", "favorite": false},
      {"en": "Switchboard", "es": "Centralita", "favorite": false},
      {"en": "Code", "es": "Código", "favorite": false},
      {"en": "To have no line", "es": "No tener línea", "favorite": false},
      {"en": "Phone book / Directory", "es": "Guía telefónica / directorio", "favorite": false},
      {"en": "Caller", "es": "Quien llama / interlocutor", "favorite": false},
      {"en": "Inviting", "es": "Invitar", "favorite": false},
      {"en": "Responding to", "es": "Responder a", "favorite": false},
      {"en": "Declining", "es": "Rechazar", "favorite": false}
    ];

    const STORAGE_KEY = "flashcards_deck_data";
    let cards = [];
    let deck = [];
    let history = [];
    let currentCard = null;
    let showingFront = true;
    let isAnimating = false;
    let onlyFavorites = false;
    let correctCount = 0;
    let wrongCount = 0;
    let totalCardsCount = 0;

    // Carga de datos
    function loadData() {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        try {
          cards = JSON.parse(stored);
          return;
        } catch (e) {
          console.error(e);
        }
      }
      cards = JSON.parse(JSON.stringify(INITIAL_DATA));
      saveData();
    }

    function saveData() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cards));
    }

    // Algoritmo de barajado Fisher-Yates
    function shuffle(arr) {
      for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
      }
    }

    function resetDeck(favsMode = false) {
      onlyFavorites = favsMode;
      correctCount = 0;
      wrongCount = 0;
      history = [];

      if (onlyFavorites) {
        const favs = cards.filter(c => c.favorite);
        if (favs.length === 0) {
          alert("Aún no tienes tarjetas marcadas con estrella (⭐).");
          onlyFavorites = false;
          deck = [...cards];
        } else {
          deck = [...favs];
        }
      } else {
        deck = [...cards];
      }

      shuffle(deck);
      totalCardsCount = deck.length;
      nextCard();
      updateModeBtnText();
    }

    function nextCard() {
      if (deck.length === 0) {
        currentCard = null;
        renderCard();
        updateUI();
        return;
      }
      currentCard = deck[0];
      showingFront = true;
      renderCard();
      updateUI();
    }

    function renderCard() {
      const cardEl = document.getElementById("cardElement");
      const textEl = document.getElementById("cardText");
      const starBadge = document.getElementById("cardStarBadge");

      if (!currentCard) {
        cardEl.className = "card front";
        textEl.innerHTML = `
          <div class="deck-finished">
            ¡Mazo completado!<br><br>
            ✓ Acertadas: ${correctCount} &nbsp;&nbsp; ✕ Repeticiones: ${wrongCount}<br><br>
            <span style="font-size:15px; color:#aaa; font-weight:400;">Pulsa ⋯ para reiniciar el mazo.</span>
          </div>`;
        starBadge.classList.remove("active");
        return;
      }

      cardEl.className = `card ${showingFront ? "front" : "back"}`;
      textEl.innerText = showingFront ? currentCard.en : currentCard.es;

      if (currentCard.favorite) {
        starBadge.classList.add("active");
      } else {
        starBadge.classList.remove("active");
      }
    }

    function flipCard() {
      if (!currentCard || isAnimating) return;
      showingFront = !showingFront;
      renderCard();
    }

    function animateFall(onComplete) {
      if (isAnimating) return;
      isAnimating = true;
      const cardEl = document.getElementById("cardElement");
      cardEl.classList.add("anim-fall");

      setTimeout(() => {
        cardEl.classList.remove("anim-fall");
        isAnimating = false;
        if (onComplete) onComplete();
      }, 160);
    }

    function markCorrect() {
      if (!currentCard || deck.length === 0 || isAnimating) return;
      animateFall(() => {
        const card = deck.shift();
        history.push({ type: "correct", card });
        correctCount++;
        nextCard();
      });
    }

    function markWrong() {
      if (!currentCard || deck.length === 0 || isAnimating) return;
      animateFall(() => {
        const card = deck.shift();
        deck.push(card);
        history.push({ type: "wrong", card });
        wrongCount++;
        nextCard();
      });
    }

    function previousCard() {
      if (history.length === 0 || isAnimating) return;
      const last = history.pop();
      if (last.type === "correct") {
        correctCount = Math.max(0, correctCount - 1);
        deck.unshift(last.card);
      } else if (last.type === "wrong") {
        wrongCount = Math.max(0, wrongCount - 1);
        if (deck.length > 0 && deck[deck.length - 1] === last.card) {
          deck.pop();
        }
        deck.unshift(last.card);
      }
      nextCard();
    }

    function toggleFavorite() {
      if (!currentCard) return;
      currentCard.favorite = !currentCard.favorite;

      const found = cards.find(c => c.en === currentCard.en);
      if (found) found.favorite = currentCard.favorite;

      saveData();
      renderCard();
      updateUI();
    }

    function updateUI() {
      const stats = document.getElementById("statsDisplay");
      const btnPrev = document.getElementById("btnPrev");
      const btnFav = document.getElementById("btnFav");

      const currentIdx = deck.length > 0 ? (totalCardsCount - deck.length + 1) : 0;
      stats.innerHTML = `${currentIdx} de ${totalCardsCount} &nbsp;|&nbsp; ✓ ${correctCount} &nbsp;✕ ${wrongCount}`;

      btnPrev.disabled = history.length === 0;

      if (currentCard && currentCard.favorite) {
        btnFav.innerText = "★";
        btnFav.classList.add("active");
      } else {
        btnFav.innerText = "☆";
        btnFav.classList.remove("active");
      }
    }

    // Pronunciación de voz nativa iOS / Web Speech API (US English)
    function speakCard() {
      if (!currentCard || !window.speechSynthesis) return;
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(currentCard.en);
      utterance.lang = "en-US";
      utterance.rate = 0.95;

      const voices = window.speechSynthesis.getVoices();
      const usVoice = voices.find(v => v.lang === "en-US" || v.lang === "en_US");
      if (usVoice) utterance.voice = usVoice;

      window.speechSynthesis.speak(utterance);
    }

    // Menú y Navegación
    function openMenu() {
      document.getElementById("menuModal").classList.add("open");
    }

    function closeModals(e) {
      if (!e || e.target.classList.contains("modal-overlay") || e.target.tagName === "BUTTON") {
        document.getElementById("menuModal").classList.remove("open");
        document.getElementById("managerModal").classList.remove("open");
      }
    }

    function toggleMode() {
      closeModals();
      resetDeck(!onlyFavorites);
    }

    function updateModeBtnText() {
      const btn = document.getElementById("btnToggleMode");
      if (onlyFavorites) {
        btn.innerText = "📚 Estudiar todas las tarjetas";
      } else {
        btn.innerText = "⭐ Estudiar solo favoritas";
      }
    }

    // Gestor / Buscador
    function openManager() {
      closeModals();
      document.getElementById("managerModal").classList.add("open");
      document.getElementById("searchInput").value = "";
      renderManagerList();
    }

    function renderManagerList() {
      const query = (document.getElementById("searchInput").value || "").toLowerCase().trim();
      const container = document.getElementById("cardsListContainer");
      container.innerHTML = "";

      const filtered = cards.filter(c => 
        !query || c.en.toLowerCase().includes(query) || c.es.toLowerCase().includes(query)
      );

      filtered.forEach(c => {
        const item = document.createElement("div");
        item.className = "list-item";
        item.innerHTML = `
          <div class="list-item-content">
            <div class="list-en">${escapeHtml(c.en)}</div>
            <div class="list-es">${escapeHtml(c.es)}</div>
          </div>
          <div class="list-actions">
            <button class="btn-tiny ${c.favorite ? "fav-active" : ""}" onclick="toggleFavFromList('${escapeParam(c.en)}')">${c.favorite ? "★" : "☆"}</button>
            <button class="btn-tiny del-btn" onclick="deleteFromList('${escapeParam(c.en)}')">🗑️</button>
          </div>
        `;
        container.appendChild(item);
      });
    }

    function toggleFavFromList(enWord) {
      const card = cards.find(c => c.en === enWord);
      if (card) {
        card.favorite = !card.favorite;
        if (currentCard && currentCard.en === enWord) {
          currentCard.favorite = card.favorite;
        }
        saveData();
        renderManagerList();
        renderCard();
        updateUI();
      }
    }

    function deleteFromList(enWord) {
      if (!confirm(`¿Eliminar "${enWord}"?`)) return;
      cards = cards.filter(c => c.en !== enWord);
      saveData();
      renderManagerList();
      resetDeck(onlyFavorites);
    }

    function addNewCard() {
      const en = prompt("Palabra o frase en inglés:");
      if (!en || !en.trim()) return;
      const es = prompt("Traducción en español:");
      if (!es || !es.trim()) return;

      cards.unshift({ en: en.trim(), es: es.trim(), favorite: false });
      saveData();
      renderManagerList();
      resetDeck(onlyFavorites);
    }

    function escapeHtml(str) {
      return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    function escapeParam(str) {
      return str.replace(/'/g, "\\'");
    }

    // Atajos de teclado (para teclado iPad/Mac o iPhone con accesorios)
    window.addEventListener("keydown", (e) => {
      if (document.querySelector(".modal-overlay.open")) return;
      if (e.code === "Space") { e.preventDefault(); flipCard(); }
      if (e.key === "ArrowLeft") markWrong();
      if (e.key === "ArrowRight") markCorrect();
      if (e.key === "Backspace") previousCard();
      if (e.key === "ArrowUp") speakCard();
      if (e.key === "f" || e.key === "F") toggleFavorite();
    });

    // Carga de voces SpeechSynthesis
    if (window.speechSynthesis) {
      window.speechSynthesis.onvoiceschanged = () => {};
    }

    // Inicialización
    loadData();
    resetDeck(false);
  </script>
</body>
</html>