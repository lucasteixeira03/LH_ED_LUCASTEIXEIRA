CREATE TABLE IF NOT EXISTS agencias (
  cod_agencia integer PRIMARY KEY,
  nome varchar(255) NOT NULL,
  endereco text,
  cidade varchar(255),
  uf char(2),
  data_abertura date,
  tipo_agencia varchar(20)
);

CREATE TABLE IF NOT EXISTS clientes (
  cod_cliente integer PRIMARY KEY,
  primeiro_nome varchar(255) NOT NULL,
  ultimo_nome varchar(255) NOT NULL,
  email varchar(255) NOT NULL,
  tipo_cliente varchar(10),
  data_inclusao timestamptz,
  cpfcnpj varchar(18) NOT NULL,
  data_nascimento date,
  endereco text,
  cep varchar(9)
);

CREATE TABLE IF NOT EXISTS colaboradores (
  cod_colaborador integer PRIMARY KEY,
  primeiro_nome varchar(255) NOT NULL,
  ultimo_nome varchar(255) NOT NULL,
  email varchar(255) NOT NULL,
  cpf varchar(14) NOT NULL,
  data_nascimento date,
  endereco text,
  cep varchar(9)
);

CREATE TABLE IF NOT EXISTS colaborador_agencia (
  cod_colaborador integer NOT NULL,
  cod_agencia integer NOT NULL
);

CREATE TABLE IF NOT EXISTS contas (
  num_conta bigint PRIMARY KEY,
  cod_cliente integer,
  cod_agencia integer,
  cod_colaborador integer,
  tipo_conta varchar(10),
  data_abertura timestamptz,
  saldo_total numeric(15,2),
  saldo_disponivel numeric(15,2),
  data_ultimo_lancamento timestamptz
);

CREATE TABLE IF NOT EXISTS propostas_credito (
  cod_proposta integer PRIMARY KEY,
  cod_cliente integer,
  cod_colaborador integer,
  data_entrada_proposta timestamptz,
  taxa_juros_mensal numeric(5,4),
  valor_proposta numeric(15,2),
  valor_financiamento numeric(15,2),
  valor_entrada numeric(15,2),
  valor_prestacao numeric(15,2),
  quantidade_parcelas integer,
  carencia integer,
  status_proposta varchar(30)
);

CREATE TABLE IF NOT EXISTS transacoes (
  cod_transacao bigint PRIMARY KEY,
  num_conta bigint,
  data_transacao timestamptz,
  nome_transacao text,
  valor_transacao numeric(15,2)
);
