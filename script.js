document.addEventListener("DOMContentLoaded", () => {
  const elenco = [
    { nick: "yuurih", nome: "Yuri Santos", nacionalidade: "🇧🇷 Brasil", posicao: "Rifler" },
    { nick: "KSCERATO", nome: "Kaike Cerato", nacionalidade: "🇧🇷 Brasil", posicao: "Rifler" },
    { nick: "FalleN (Capitão)", nome: "Gabriel Toledo", nacionalidade: "🇧🇷 Brasil", posicao: "Rifler" },
    { nick: "molodoy", nome: "Danil Golubenko", nacionalidade: "🇰🇿 Cazaquistão", posicao: "AWPer" },
    { nick: "YEKINDAR", nome: "Mareks Gaļinskis", nacionalidade: "🇱🇻 Letônia", posicao: "Rifler" },
    { nick: "sidde", nome: "Sid Macedo", nacionalidade: "🇧🇷 Brasil", posicao: "Treinador" },
    { nick: "Hepa", nome: "Juan Borges", nacionalidade: "🇪🇸 Espanha", posicao: "Treinador Assistente" }
  ];

  const elencoList = document.getElementById("elenco-list");

  elenco.forEach(jogador => {
    const item = document.createElement("li");
    item.textContent = `${jogador.nick} (${jogador.nome}) - ${jogador.nacionalidade} - ${jogador.posicao}`;
    elencoList.appendChild(item);
  });
});
