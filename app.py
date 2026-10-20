import tkinter as tk
from tkinter import scrolledtext, font
import threading
from groq import Groq

# Configuração da API do Groq
client = Groq(api_key='')

# System Prompt otimizado
SYSTEM_PROMPT = """
# PAPEL
Você é o Junior, um professor de música especialista em contrabaixo, guitarra, violão, canto e teoria aplicada à improvisação e escalas musicais.

# PERFIL E TOM
- Carismático, técnico, brincalhão e divertido na medida certa.
- Didático e focado inteiramente no progresso e aprendizado do aluno.

# DIRETRIZES DE ESTILO E FORMATAÇÃO (CRÍTICO)
- NUNCA utilize asteriscos (* ou **) ou qualquer marcação Markdown de negrito/itálico, pois as respostas serão lidas em voz alta ou exibidas em interfaces de texto simples.
- Não crie códigos em linguagens de programação.
- Não invente apelidos para o usuário e não exagere nas brincadeiras.

# ESPECIALIDADES
- Domínio absoluto sobre escalas, modos gregos, cadências, técnicas de execução instrumental e vocal, além de caminhos práticos para o improviso criativo.
"""

class JuniorChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professor Junior - Chat Musical")
        self.root.geometry("780x620")
        
        # --- PALETA DE CORES ---
        self.COLOR_BG = "#121214"         # Fundo principal (Fundo bem escuro)
        self.COLOR_CARD = "#1E1E24"       # Fundo das caixas e cabeçalho (Cinza escuro)
        self.COLOR_INPUT = "#2A2A32"      # Fundo do campo de entrada (Cinza médio)
        self.COLOR_BRAND_GREEN = "#00E676"# Verde (Marca/Destaques/Botão)
        self.COLOR_USER_BLUE = "#4FC3F7"  # Azul claro (Nome do usuário)
        self.COLOR_WHITE = "#FFFFFF"      # Branco puro (Respostas do Junior)
        self.COLOR_TEXT_USER = "#E0E0E0"  # Cinza claro (Perguntas do usuário)
        self.COLOR_HINT = "#A0A0A0"       # Cinza suave (Instruções/Status)

        self.root.config(bg=self.COLOR_BG)

        # Fontes
        self.font_family = "Segoe UI"
        self.title_font = font.Font(family=self.font_family, size=13, weight="bold")
        self.text_font = font.Font(family=self.font_family, size=11)
        self.bold_font = font.Font(family=self.font_family, size=11, weight="bold")

        # Cabeçalho
        header_frame = tk.Frame(root, bg=self.COLOR_CARD, pady=12, padx=15)
        header_frame.pack(fill=tk.X)
        
        self.title_label = tk.Label(
            header_frame, 
            text="🎵 Professor Junior | Baixo, Violão, Guitarra, Canto & Improviso", 
            bg=self.COLOR_CARD, 
            fg=self.COLOR_BRAND_GREEN, 
            font=self.title_font
        )
        self.title_label.pack(side=tk.LEFT)

        # Área de Chat (Histórico)
        chat_frame = tk.Frame(root, bg=self.COLOR_BG, padx=15, pady=10)
        chat_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_area = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            bg=self.COLOR_CARD, 
            fg=self.COLOR_WHITE, 
            font=self.text_font,
            insertbackground=self.COLOR_WHITE,
            relief=tk.FLAT,
            padx=12,
            pady=12
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)

        # --- TAGS DE CORES NO CHAT ---
        self.chat_area.tag_config("user_label", foreground=self.COLOR_USER_BLUE, font=self.bold_font)
        self.chat_area.tag_config("user_text", foreground=self.COLOR_TEXT_USER, font=self.text_font)
        self.chat_area.tag_config("junior_label", foreground=self.COLOR_BRAND_GREEN, font=self.bold_font)
        self.chat_area.tag_config("junior_text", foreground=self.COLOR_WHITE, font=self.text_font)
        self.chat_area.tag_config("status", foreground=self.COLOR_HINT, font=(self.font_family, 10, "italic"))

        # Rodapé / Área de Entrada
        input_frame = tk.Frame(root, bg=self.COLOR_CARD, padx=15, pady=12)
        input_frame.pack(fill=tk.X)

        self.input_field = tk.Entry(
            input_frame, 
            font=self.text_font, 
            bg=self.COLOR_INPUT, 
            fg=self.COLOR_WHITE, 
            insertbackground=self.COLOR_WHITE,
            relief=tk.FLAT
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.input_field.bind("<Return>", lambda event: self.enviar_mensagem())

        self.send_button = tk.Button(
            input_frame, 
            text="Enviar", 
            command=self.enviar_mensagem, 
            bg=self.COLOR_BRAND_GREEN, 
            fg="#121212", 
            font=font.Font(family=self.font_family, size=10, weight="bold"),
            relief=tk.FLAT,
            padx=20,
            pady=6,
            cursor="hand2"
        )
        self.send_button.pack(side=tk.RIGHT)

        # Mensagem inicial de boas-vindas do Professor Junior
        self.adicionar_mensagem("Junior: ", "Fala, músico! Beleza? Sou o Junior, pronto para destravar suas escalas, teu instrumento ou tua voz. Qual é a boa de hoje?", "junior")

    def adicionar_mensagem(self, rotulo, conteudo, remetente):
        self.chat_area.config(state=tk.NORMAL)
        
        # Posição inicial da inserção
        start_idx = self.chat_area.index(tk.END)
        
        # Insere o Rótulo (Ex: "Você: " ou "Junior: ")
        self.chat_area.insert(tk.END, f"\n{rotulo}")
        label_end_idx = self.chat_area.index(tk.END)
        
        # Insere o Conteúdo
        self.chat_area.insert(tk.END, f"{conteudo}\n")
        content_end_idx = self.chat_area.index(tk.END)

        # Aplica cores distintas ao rótulo e ao corpo do texto
        if remetente == "user":
            self.chat_area.tag_add("user_label", start_idx, label_end_idx)
            self.chat_area.tag_add("user_text", label_end_idx, content_end_idx)
        elif remetente == "junior":
            self.chat_area.tag_add("junior_label", start_idx, label_end_idx)
            self.chat_area.tag_add("junior_text", label_end_idx, content_end_idx)
        elif remetente == "status":
            self.chat_area.tag_add("status", start_idx, content_end_idx)

        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def enviar_mensagem(self):
        pergunta = self.input_field.get().strip()
        if not pergunta:
            return

        self.input_field.delete(0, tk.END)
        self.adicionar_mensagem("Você: ", pergunta, "user")
        
        # Desativa controles durante o processamento
        self.send_button.config(state=tk.DISABLED)
        self.input_field.config(state=tk.DISABLED)

        # Thread paralela para não travar a interface gráfica
        threading.Thread(target=self.processar_resposta_ia, args=(pergunta,), daemon=True).start()

    def processar_resposta_ia(self, pergunta):
        try:
            resposta = client.chat.completions.create(
                model='openai/gpt-oss-20b',
                messages=[
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': pergunta}
                ],
                temperature=1.0,
            )
            conteudo_resposta = resposta.choices[0].message.content
            self.root.after(0, self.atualizar_interface_sucesso, conteudo_resposta)
        except Exception as e:
            erro_msg = f"Eita, deu uma pane aqui nos meus cabos. Erro: {e}"
            self.root.after(0, self.atualizar_interface_sucesso, erro_msg)

    def atualizar_interface_sucesso(self, resposta_texto):
        self.adicionar_mensagem("Junior: ", resposta_texto, "junior")
        self.send_button.config(state=tk.NORMAL)
        self.input_field.config(state=tk.NORMAL)
        self.input_field.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = JuniorChatApp(root)
    root.mainloop()