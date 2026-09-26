const API_URL = window.location.port === '8001' ? 'http://127.0.0.1:8000' : window.location.origin;
const DEMO_PROJECT = {
  idea: 'A platform that helps college students find the right teammates for hackathons.',
  audience: 'college students',
  industry: 'education',
  problem: 'Students struggle to find complementary skills and trustworthy teammates before deadlines.',
};
const authState = { token: localStorage.getItem('brandforge_token'), user: null, mode: 'login', afterAuth: null };

const stages = [
  {
    key: 'discover',
    title: 'Discover',
    description: 'Capture the raw idea, audience, and problem to build a grounded strategic foundation.',
    fields: [
      { key: 'idea', label: 'Raw idea', type: 'textarea', placeholder: 'A platform that helps college students find the right teammates for hackathons.', required: true },
      { key: 'audience', label: 'Target audience', type: 'text', placeholder: 'college students' },
      { key: 'industry', label: 'Industry', type: 'text', placeholder: 'education' },
      { key: 'problem', label: 'Problem', type: 'textarea', placeholder: 'Students struggle to find complementary skills and trustworthy teammates before deadlines.' }
    ]
  },
  {
    key: 'position',
    title: 'Position',
    description: 'Translate the discovery into a sharp position in the market and highlight the strongest strategic angle.',
    fields: []
  },
  {
    key: 'define',
    title: 'Define',
    description: 'Establish the mission, principles, and brand qualities that shape the voice and direction.',
    fields: []
  },
  {
    key: 'express',
    title: 'Express',
    description: 'Generate naming, messaging, and visual concepts that turn strategy into a compelling identity.',
    fields: []
  },
  {
    key: 'challenge',
    title: 'Challenge',
    description: 'Stress test the brand for contradictions, fit, and opportunities for sharper differentiation.',
    fields: []
  },
  {
    key: 'finalize',
    title: 'Deliver',
    description: 'Finalize the complete brand system and export a polished brief for handoff.',
    fields: []
  },
  {
    key: 'launch',
    title: 'Launch',
    description: 'Turn the finished brand system into a focused launch plan with channels, checklist, and success signals.',
    fields: []
  }
];

const state = {
  projectId: null,
  project: null,
  currentStageIndex: 0,
  stageResults: {},
  loading: false,
};

const landing = document.querySelector('.landing-page');
const workspace = document.getElementById('workspace');
const startBtn = document.getElementById('start-building');
const workflowBtn = document.getElementById('show-workflow');
const demoCta = document.getElementById('demo-cta');
const stageList = document.getElementById('stage-list');
const stageTitle = document.getElementById('stage-title');
const stageKicker = document.getElementById('stage-kicker');
const stageDescription = document.getElementById('stage-description');
const fieldGrid = document.getElementById('field-grid');
const resultsCard = document.getElementById('results-card');
const resultsContent = document.getElementById('results-content');
const errorCard = document.getElementById('error-card');
const continueBtn = document.getElementById('continue-stage');
const backBtn = document.getElementById('back-stage');
const saveBtn = document.getElementById('save-project');
const exportBtn = document.getElementById('export-project');
const copyBtn = document.getElementById('copy-project');
const newProjectBtn = document.getElementById('new-project');
const projectHistory = document.getElementById('project-history');
const overviewProject = document.getElementById('overview-project');
const overviewProgress = document.getElementById('overview-progress');
const overviewStatus = document.getElementById('overview-status');
const overviewProgressBar = document.getElementById('overview-progress-bar');
const workflowSignal = document.getElementById('workflow-signal');
const authModal = document.getElementById('auth-modal');
const authForm = document.getElementById('auth-form');
const authNameField = document.querySelector('.auth-name-field');
const authName = document.getElementById('auth-name');
const authEmail = document.getElementById('auth-email');
const authPassword = document.getElementById('auth-password');
const authTitle = document.getElementById('auth-title');
const authSubtitle = document.getElementById('auth-subtitle');
const authSubmit = document.getElementById('auth-submit');
const authSwitch = document.getElementById('auth-switch');
const authError = document.getElementById('auth-error');

function openAuth(mode = 'login', afterAuth = null) {
  authState.mode = mode;
  authState.afterAuth = afterAuth;
  authModal.classList.remove('hidden');
  authNameField.classList.toggle('hidden', mode !== 'signup');
  authTitle.textContent = mode === 'signup' ? 'Create your strategy workspace.' : 'Welcome back to BrandForge.';
  authSubtitle.textContent = mode === 'signup'
    ? 'Save projects, revisit decisions, and keep your brand strategy in one place.'
    : 'Log in to continue building your brand system.';
  authSubmit.textContent = mode === 'signup' ? 'Create account' : 'Log in';
  authSwitch.innerHTML = mode === 'signup'
    ? 'Already have an account? <button type="button" id="switch-auth">Log in</button>'
    : 'New to BrandForge? <button type="button" id="switch-auth">Create an account</button>';
  document.getElementById('switch-auth').addEventListener('click', () => openAuth(mode === 'signup' ? 'login' : 'signup', afterAuth));
  authError.classList.add('hidden');
  authForm.reset();
  authEmail.focus();
}

function requireAuth(action) {
  if (authState.token) action();
  else openAuth('signup', action);
}

function toggleLanding(show) {
  landing.classList.toggle('hidden', !show);
  workspace.classList.toggle('hidden', show);
}

function showError(message) {
  errorCard.textContent = message;
  errorCard.classList.remove('hidden');
}

function showSavedMessage(message) {
  showError(message);
  errorCard.classList.add('saved-message');
}

function clearError() {
  errorCard.classList.add('hidden');
  errorCard.classList.remove('saved-message');
  errorCard.textContent = '';
}

function stageIndexForProject(project) {
  const stageMap = {
    deliver: 'launch',
    complete: 'launch',
  };
  const stage = stageMap[project.workflow_stage] || project.workflow_stage;
  const index = stages.findIndex((item) => item.key === stage);
  return index < 0 ? 0 : index;
}

async function loadProjectHistory() {
  try {
    const response = await fetch(`${API_URL}/api/projects`);
    if (!response.ok) return;

    const data = await response.json();
    projectHistory.innerHTML = '<option value="">Recent projects</option>';
    data.projects.forEach((project) => {
      const option = document.createElement('option');
      option.value = project.project_id;
      option.textContent = project.final_brand_system?.brand_name || project.idea.slice(0, 34);
      projectHistory.appendChild(option);
    });
  } catch {
    // Project history is optional; the workspace remains usable offline.
  }
}

async function openProject(projectId) {
  if (!projectId) return;
  const response = await fetch(`${API_URL}/api/projects/${projectId}`);
  if (!response.ok) {
    showError('We couldn’t open that project.');
    return;
  }

  state.project = await response.json();
  state.projectId = state.project.project_id;
  state.currentStageIndex = stageIndexForProject(state.project);
  const resultKey = stages[state.currentStageIndex].key;
  const resultMap = {
    discover: 'discovery',
    position: 'positioning',
    define: 'brand_definition',
    express: 'expression',
    challenge: 'challenge',
    finalize: 'final_brand_system',
    launch: 'launch',
  };
  const stageData = state.project[resultMap[resultKey]];
  const hasStageData = stageData && Object.keys(stageData).length > 0;
  state.stageResults[resultKey] = hasStageData ? stageData : (resultKey === 'launch' ? state.project.final_brand_system : null);
  state.finalExport = state.project.final_brand_system || null;
  toggleLanding(false);
  renderStageList();
  renderStageForm();
  renderResults(state.stageResults[resultKey]);
}

function resetProject() {
  state.projectId = null;
  state.project = null;
  state.currentStageIndex = 0;
  state.stageResults = {};
  state.finalExport = null;
  projectHistory.value = '';
  resultsCard.classList.add('hidden');
  clearError();
  toggleLanding(false);
  renderStageForm();
  renderStageList();
}

function fillProjectForm(project) {
  Object.entries(project).forEach(([key, value]) => {
    const input = document.getElementById(key);
    if (input) input.value = value || '';
  });
}

function renderStageList() {
  const items = stageList.querySelectorAll('li');
  items.forEach((item, index) => {
    const dot = item.querySelector('.dot');
    const check = index < state.currentStageIndex;
    const active = index === state.currentStageIndex;
    item.classList.toggle('active', active);
    dot.textContent = check ? '✓' : '○';
  });
  const completed = state.currentStageIndex;
  const total = stages.length;
  const projectName = state.project?.final_brand_system?.brand_name || state.project?.idea?.slice(0, 28) || 'New brand project';
  const status = completed === 0 ? 'Ready to begin' : completed >= total - 1 ? 'Launch-ready' : 'In progress';
  overviewProject.textContent = projectName;
  overviewProgress.textContent = `${completed} / ${total} stages`;
  overviewStatus.textContent = status;
  overviewProgressBar.style.width = `${Math.max(4, (completed / total) * 100)}%`;
  workflowSignal.textContent = completed === 0
    ? 'Your strategy is waiting for its first input.'
    : `Stage ${String(completed + 1).padStart(2, '0')} is shaping your brand direction.`;
}

function renderStageForm() {
  const stage = stages[state.currentStageIndex];
  stageTitle.textContent = stage.title;
  stageKicker.textContent = `Stage ${String(state.currentStageIndex + 1).padStart(2, '0')}`;
  stageDescription.textContent = stage.description;
  fieldGrid.innerHTML = '';

  if (stage.fields.length) {
    stage.fields.forEach((field) => {
      const wrap = document.createElement('div');
      wrap.className = `field ${field.type === 'textarea' ? 'full' : ''}`;

      const label = document.createElement('label');
      label.textContent = field.label;
      label.htmlFor = field.key;

      const input = document.createElement(field.type === 'textarea' ? 'textarea' : 'input');
      input.id = field.key;
      input.name = field.key;
      input.placeholder = field.placeholder || '';
      if (field.type !== 'textarea') input.type = field.type;
      input.value = state.project ? (state.project[field.key] || '') : '';

      wrap.append(label, input);
      fieldGrid.appendChild(wrap);
    });
  }
}

function renderResults(data) {
  resultsCard.classList.remove('hidden');
  resultsContent.innerHTML = '';

  if (!data || !Object.keys(data).length) {
    resultsContent.innerHTML = '<p>No generated insight yet.</p>';
    return;
  }

  const cards = [];

  if (data.problem_statement) {
    cards.push({ label: 'Problem', title: 'Problem', body: `<p>${data.problem_statement}</p>`, isList: false });
  }
  if (data.primary_audience) {
    cards.push({ label: 'Audience', title: 'Primary audience', body: `<p>${data.primary_audience}</p>`, isList: false });
  }
  if (data.positioning_statement) {
    cards.push({ label: 'Positioning', title: 'Positioning', body: `<p>${data.positioning_statement}</p>`, isList: false });
  }
  if (data.mission) {
    cards.push({ label: 'Mission', title: 'Mission', body: `<p>${data.mission}</p>`, isList: false });
  }
  if (data.brand_name) {
    cards.push({ label: 'Brand system', title: 'Final brand system', body: `<p><strong>${data.brand_name}</strong> — ${data.tagline}</p>`, isList: false });
  }

  if (data.user_pain_points) {
    cards.push({ label: 'Pain points', title: 'Pain points', body: `<ul>${data.user_pain_points.map((item) => `<li>${item}</li>`).join('')}</ul>`, isList: true });
  }
  if (data.user_needs) {
    cards.push({ label: 'User needs', title: 'User needs', body: `<ul>${data.user_needs.map((item) => `<li>${item}</li>`).join('')}</ul>`, isList: true });
  }
  if (data.brand_personality) {
    cards.push({ label: 'Personality', title: 'Brand personality', body: `<ul>${data.brand_personality.map((item) => `<li>${item}</li>`).join('')}</ul>`, isList: true });
  }
  if (data.messaging_pillars) {
    cards.push({ label: 'Pillars', title: 'Messaging pillars', body: `<ul>${data.messaging_pillars.map((item) => `<li>${item}</li>`).join('')}</ul>`, isList: true });
  }
  if (data.important_questions) {
    cards.push({ label: 'Questions', title: 'Important questions', body: `<ul>${data.important_questions.map((item) => `<li>${item}</li>`).join('')}</ul>`, isList: true });
  }
  if (data.key_issue) {
    cards.push({ label: 'Stress test', title: 'Key issue', body: `<p>${data.key_issue}</p>`, isList: false });
  }
  if (data.recommended_changes) {
    cards.push({ label: 'Recommendations', title: 'Recommended change', body: `<ul>${data.recommended_changes.map((item) => `<li>${item}</li>`).join('')}</ul>`, isList: true });
  }
  if (data.launch_summary) {
    cards.push({ label: 'Launch', title: 'Launch summary', body: `<p>${data.launch_summary}</p>`, isList: false });
  }
  if (data.launch_goal) {
    cards.push({ label: 'Launch goal', title: 'Launch goal', body: `<p>${data.launch_goal}</p>`, isList: false });
  }
  if (data.launch_channels) {
    cards.push({ label: 'Channels', title: 'Launch channels', body: `<ul>${data.launch_channels.map((item) => `<li>${item}</li>`).join('')}</ul>`, isList: true });
  }
  if (data.launch_messaging) {
    cards.push({
      label: 'Messaging',
      title: 'Launch messaging',
      body: `<p><strong>${data.launch_messaging.headline || ''}</strong></p><p>${data.launch_messaging.primary_pitch || ''}</p><p><em>${data.launch_messaging.cta || ''}</em></p>`,
      isList: false,
    });
  }
  if (data.launch_checklist) {
    cards.push({ label: 'Checklist', title: 'Launch checklist', body: `<ul>${data.launch_checklist.map((item) => `<li>${item}</li>`).join('')}</ul>`, isList: true });
  }
  if (data.success_metrics) {
    cards.push({ label: 'Metrics', title: 'Success metrics', body: `<ul>${data.success_metrics.map((item) => `<li>${item}</li>`).join('')}</ul>`, isList: true });
  }
  if (data.launch_timeline) {
    cards.push({ label: 'Timeline', title: 'Launch timeline', body: `<ul>${data.launch_timeline.map((item) => `<li>${item}</li>`).join('')}</ul>`, isList: true });
  }

  const container = document.createElement('div');
  container.className = 'result-group';
  cards.forEach((card) => {
    const box = document.createElement('div');
    box.className = 'info-card';
    box.innerHTML = `<span class="label">${card.label}</span><h4>${card.title}</h4>${card.body}`;
    container.appendChild(box);
  });
  resultsContent.appendChild(container);
}

async function createProject() {
  const idea = document.getElementById('idea')?.value?.trim();
  if (!idea) {
    showError('Please enter a raw idea before continuing.');
    return null;
  }

  const payload = {
    idea,
    audience: document.getElementById('audience')?.value?.trim() || null,
    industry: document.getElementById('industry')?.value?.trim() || null,
    problem: document.getElementById('problem')?.value?.trim() || null,
  };

  const response = await fetch(`${API_URL}/api/projects`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error('We couldn’t create the project. Please try again.');
  }

  const result = await response.json();
  state.projectId = result.project_id;
  state.project = result;
  await loadProjectHistory();
  projectHistory.value = state.projectId;
  renderStageList();
  return result;
}

async function startDemoProject() {
  resetProject();
  fillProjectForm(DEMO_PROJECT);
  await continueWorkflow();
}

async function saveProjectDetails() {
  if (!state.projectId) return true;
  const payload = {
    idea: document.getElementById('idea')?.value?.trim(),
    audience: document.getElementById('audience')?.value?.trim() || null,
    industry: document.getElementById('industry')?.value?.trim() || null,
    problem: document.getElementById('problem')?.value?.trim() || null,
  };
  const response = await fetch(`${API_URL}/api/projects/${state.projectId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error('We couldn’t save the project details.');
  state.project = await response.json();
  return true;
}

async function callStage(stageKey) {
  if (!state.projectId) {
    return;
  }

  state.loading = true;
  continueBtn.disabled = true;
  continueBtn.textContent = 'Analyzing your idea...';
  clearError();

  try {
    const response = await fetch(`${API_URL}/api/projects/${state.projectId}/${stageKey}`, {
      method: 'POST',
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'We couldn’t complete this stage.' }));
      throw new Error(error.detail || 'We couldn’t complete this stage.');
    }

    const payload = await response.json();
    state.stageResults[stageKey] = payload.data;
    renderResults(payload.data);
    if (stageKey === 'launch') {
      const exportResponse = await fetch(`${API_URL}/api/projects/${state.projectId}/export`);
      const exportData = await exportResponse.json();
      state.finalExport = exportData.final_brand_system;
    }
    return payload;
  } catch (error) {
    showError(error.message || 'We couldn’t complete this stage.');
    return null;
  } finally {
    state.loading = false;
    continueBtn.disabled = false;
    continueBtn.textContent = 'Continue →';
  }
}

async function continueWorkflow() {
  if (state.loading) return;
  const currentKey = stages[state.currentStageIndex].key;

  if (state.currentStageIndex === 0 && !state.projectId) {
    const created = await createProject();
    if (!created) return;
  }

  if (state.currentStageIndex === 0) {
    const generated = await callStage(currentKey);
    if (!generated) return;
  } else {
    const generated = await callStage(currentKey);
    if (!generated) return;
  }

  if (state.currentStageIndex < stages.length - 1) {
    state.currentStageIndex += 1;
    renderStageList();
    renderStageForm();
  } else {
    state.currentStageIndex = stages.length - 1;
    renderStageList();
    renderStageForm();
  }
}

backBtn.addEventListener('click', () => {
  if (state.currentStageIndex > 0) {
    state.currentStageIndex -= 1;
    renderStageList();
    renderStageForm();
  }
});

saveBtn.addEventListener('click', async () => {
  try {
    if (!state.projectId) {
      const created = await createProject();
      if (!created) return;
    } else {
      await saveProjectDetails();
    }
    await loadProjectHistory();
    projectHistory.value = state.projectId;
    showError('Project saved to your local BrandForge workspace.');
    errorCard.classList.add('saved-message');
  } catch (error) {
    showError(error.message || 'We couldn’t save the project.');
  }
});

exportBtn.addEventListener('click', async () => {
  if (!state.projectId || !state.finalExport) {
    showError('Finish the workflow before exporting the brief.');
    return;
  }
  const response = await fetch(`${API_URL}/api/projects/${state.projectId}/export`);
  if (!response.ok) {
    showError('We couldn’t prepare the export.');
    return;
  }
  const data = await response.json();
  const blob = new Blob([data.markdown_export], { type: 'text/markdown' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${data.final_brand_system.brand_name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-brand-brief.md`;
  link.click();
  URL.revokeObjectURL(link.href);
});

copyBtn.addEventListener('click', async () => {
  if (!state.projectId || !state.finalExport) {
    showError('Finish the workflow before copying the brief.');
    return;
  }
  try {
    const response = await fetch(`${API_URL}/api/projects/${state.projectId}/export`);
    if (!response.ok) throw new Error('We couldn’t prepare the brief.');
    const data = await response.json();
    await navigator.clipboard.writeText(data.markdown_export);
    showSavedMessage('Brand brief copied to your clipboard.');
  } catch (error) {
    showError(error.message || 'We couldn’t copy the brief.');
  }
});

projectHistory.addEventListener('change', (event) => openProject(event.target.value));
newProjectBtn.addEventListener('click', resetProject);

startBtn.addEventListener('click', () => {
  requireAuth(() => resetProject());
});

workflowBtn.addEventListener('click', () => {
  startDemoProject();
});

demoCta.addEventListener('click', () => {
  requireAuth(startDemoProject);
});

document.getElementById('login-button').addEventListener('click', () => openAuth('login'));
document.getElementById('signup-button').addEventListener('click', () => openAuth('signup'));
document.getElementById('auth-close').addEventListener('click', () => authModal.classList.add('hidden'));
authModal.addEventListener('click', (event) => {
  if (event.target === authModal) authModal.classList.add('hidden');
});
authForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  authSubmit.disabled = true;
  authError.classList.add('hidden');
  try {
    const endpoint = authState.mode === 'signup' ? '/api/auth/signup' : '/api/auth/login';
    const body = authState.mode === 'signup'
      ? { name: authName.value.trim(), email: authEmail.value.trim(), password: authPassword.value }
      : { email: authEmail.value.trim(), password: authPassword.value };
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Authentication failed.');
    authState.token = data.access_token;
    authState.user = data.user;
    localStorage.setItem('brandforge_token', authState.token);
    authModal.classList.add('hidden');
    if (authState.afterAuth) authState.afterAuth();
  } catch (error) {
    authError.textContent = error.message;
    authError.classList.remove('hidden');
  } finally {
    authSubmit.disabled = false;
  }
});

continueBtn.addEventListener('click', continueWorkflow);

renderStageList();
renderStageForm();
loadProjectHistory();
