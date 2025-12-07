#  Academia Dev Python – Sistema de Gestão Acadêmica

Sistema web completo para gerenciamento de **alunos, cursos e matrículas**, desenvolvido para o desafio técnico **Academia Dev Python – Estágio 2026.1**.

Inclui backend em **Django + Django REST Framework**, templates HTML, autenticação, API RESTful, relatórios SQL brutos e ambiente totalmente **Dockerizado**.

---

## 🚀 Funcionalidades do Sistema

### 👤 1. Gestão de Alunos
- Criar aluno **(rota aberta)**  
- Listar alunos **(autenticado)**  
- Atualizar e remover alunos **(somente admin)**  
- Cada aluno possui:
  - Nome  
  - Email  
  - CPF  
  - Data de ingresso  
  - Usuário vinculado (para login)

---

### 📘 2. Gestão de Cursos
- Criar, listar e atualizar cursos  
- **Apenas admin** pode criar, editar e remover  
- Campos:
  - Nome  
  - Carga horária  
  - Valor da inscrição  
  - Status (ativo/inativo)

---

### 🧾 3. Matrículas
- Aluno autenticado pode se matricular  
- Valor é calculado automaticamente  
- Status inicial: **pendente**  
- Um aluno não pode se matricular duas vezes no mesmo curso  
- Admin visualiza todas  
- Usuário comum vê apenas as suas matrículas  

---

### 💳 4. Controle de Pagamentos
- Endpoint para marcar matrícula como **paga**  
- Apenas admin pode alterar

---

### 📊 5. Relatórios (SQL Bruto)
Relatório exigido pelo desafio:

**Total de matrículas por curso, ordenado pela maior quantidade.**

Endpoint:
    GET /api/relatorios/total-matriculas/

### 🖥️ 6. Templates HTML

#### ✔️ dashboard.html  
Exibe:
- Total de alunos  
- Total de cursos  
- Total de matrículas  
- Total arrecadado  
- Estatísticas gerais  

#### ✔️ aluno_historico.html  
Exibe:
- Dados do aluno  
- Suas matrículas  
- Status do pagamento  
- Datas e valores  

---

## 🧱 Modelos do Sistema

### Aluno
id, nome, email, cpf, data_ingresso, user

### Curso
id, nome, carga_horaria, valor_inscricao, status

### Matricula
id, aluno (FK), curso (FK), data_matricula, valor, status_pagamento


---

## 🌐 Endpoints da API

### 🔹 Alunos – `/api/alunos/`
| Método | Rota | Acesso |
|--------|------|--------|
| POST | `/api/alunos/` | Público |
| GET | `/api/alunos/` | Autenticado |
| GET | `/api/alunos/{id}/` | Autenticado |
| PUT/PATCH/DELETE | `/api/alunos/{id}/` | Admin |

---

### 🔹 Cursos – `/api/cursos/`
| Método | Rota | Acesso |
|--------|------|--------|
| GET | `/api/cursos/` | Autenticado |
| POST/PUT/DELETE | `/api/cursos/` | Admin |

---

### 🔹 Matrículas – `/api/matriculas/`
| Método | Rota | Acesso |
|--------|------|--------|
| POST | `/api/matriculas/` | Autenticado |
| GET | `/api/matriculas/` | Usuário vê só as suas / Admin vê todas |
| GET | `/api/matriculas/{id}/` | Autenticado |
| POST | `/api/matriculas/{id}/marcar-paga/` | Admin |
| GET | `/api/matriculas/aluno/{id}/` | Dono ou admin |
| GET | `/api/relatorios/total-matriculas/` | SQL Bruto |

---

## 🐳 Ambiente Docker

### 📌 Requisitos
- Docker  
- Docker Compose  

### ▶️ Rodar o projeto
```bash
docker compose up --build

## Criar superusuário
docker exec -it academia_dev_python_backend python manage.py createsuperuser
```