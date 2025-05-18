const BASE_URL = 'http://localhost:8000';

export async function fetchIssues() {
  const response = await fetch(`${BASE_URL}/fetch-issues`);
  return await response.json();
}

export async function fetchProjects() {
  const response = await fetch(`${BASE_URL}/fetch-projects`);
  return await response.json();
}

export async function fetchBoards() {
  const response = await fetch(`${BASE_URL}/fetch-boards`);
  return await response.json();
}
