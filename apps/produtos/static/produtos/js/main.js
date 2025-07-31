/**
 * JavaScript principal para o Sistema de Produtos
 * Django 4.x + DRF + Bootstrap 5
 */

// Configurações globais
const CONFIG = {
    API_BASE_URL: '/api/produtos/',
    API_RISCO_URL: '/api/produtos/risco/',
    CSRF_TOKEN: getCookie('csrftoken')
};

/**
 * Função para obter cookie CSRF
 * @param {string} name - Nome do cookie
 * @returns {string|null} - Valor do cookie ou null
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Função para mostrar alertas
 * @param {string} message - Mensagem do alerta
 * @param {string} type - Tipo do alerta (success, danger, warning, info)
 * @param {string} containerId - ID do container (opcional)
 */
function showAlert(message, type = 'info', containerId = 'alert-container') {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="fas fa-${getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    container.innerHTML = alertHtml;
}

/**
 * Função para obter ícone do alerta
 * @param {string} type - Tipo do alerta
 * @returns {string} - Nome do ícone
 */
function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Função para fazer requisições HTTP
 * @param {string} url - URL da requisição
 * @param {Object} options - Opções da requisição
 * @returns {Promise} - Promise com a resposta
 */
async function fetchAPI(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CONFIG.CSRF_TOKEN
        }
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, finalOptions);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(Object.values(errorData).flat().join(', '));
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro na requisição:', error);
        throw error;
    }
}

/**
 * Função para formatar data
 * @param {string} dateString - String da data
 * @returns {string} - Data formatada
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Função para validar percentual
 * @param {number} value - Valor a ser validado
 * @param {number} min - Valor mínimo
 * @param {number} max - Valor máximo
 * @returns {boolean} - Se é válido
 */
function validatePercentage(value, min = 0, max = 100) {
    return !isNaN(value) && value >= min && value <= max;
}

/**
 * Função para debounce
 * @param {Function} func - Função a ser executada
 * @param {number} wait - Tempo de espera em ms
 * @returns {Function} - Função com debounce
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Função para mostrar loading
 * @param {string} elementId - ID do elemento
 * @param {boolean} show - Se deve mostrar ou esconder
 */
function toggleLoading(elementId, show = true) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    if (show) {
        element.classList.remove('d-none');
    } else {
        element.classList.add('d-none');
    }
}

/**
 * Função para validar formulário
 * @param {HTMLFormElement} form - Formulário a ser validado
 * @returns {boolean} - Se é válido
 */
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

/**
 * Função para limpar formulário
 * @param {HTMLFormElement} form - Formulário a ser limpo
 */
function clearForm(form) {
    form.reset();
    form.querySelectorAll('.is-invalid').forEach(field => {
        field.classList.remove('is-invalid');
    });
}

/**
 * Função para criar badge
 * @param {string} text - Texto do badge
 * @param {string} type - Tipo do badge
 * @returns {string} - HTML do badge
 */
function createBadge(text, type = 'secondary') {
    return `<span class="badge bg-${type}">${text}</span>`;
}

/**
 * Função para verificar se produto tem risco
 * @param {Object} produto - Objeto do produto
 * @returns {boolean} - Se tem risco
 */
function hasRisk(produto) {
    return produto.thc_percentual > 0.3 && 
           ['neurologia', 'pediatria'].includes(produto.categoria_terapeutica);
}

/**
 * Função para obter classe de risco
 * @param {Object} produto - Objeto do produto
 * @returns {string} - Classe CSS
 */
function getRiskClass(produto) {
    return hasRisk(produto) ? 'table-danger' : '';
}

/**
 * Função para obter cor do badge THC
 * @param {number} thc - Valor do THC
 * @returns {string} - Classe do badge
 */
function getThcBadgeClass(thc) {
    return thc > 0.3 ? 'bg-warning' : 'bg-success';
}

/**
 * Função para obter cor do badge status ANVISA
 * @param {string} status - Status ANVISA
 * @returns {string} - Classe do badge
 */
function getStatusBadgeClass(status) {
    const classes = {
        'aprovado': 'bg-success',
        'pendente': 'bg-warning',
        'reprovado': 'bg-danger'
    };
    return classes[status] || 'bg-secondary';
}

// Event listeners globais
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Inicializar popovers do Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Exportar funções para uso global
window.ProdutoUtils = {
    showAlert,
    fetchAPI,
    formatDate,
    validatePercentage,
    debounce,
    toggleLoading,
    validateForm,
    clearForm,
    createBadge,
    hasRisk,
    getRiskClass,
    getThcBadgeClass,
    getStatusBadgeClass,
    getCookie
}; 