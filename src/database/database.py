from contextlib import contextmanager
from typing import Any, Union

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.utils.logger import logger


class ConnessioneDatabase:
    """Gestisce l'apertura e la chiusura della connessione al database."""

    def __init__(self, config) -> None:
        try:
            self.engine: Engine = create_engine(
                f"mysql+mysqlconnector://{config['user']}:{config['password']}@"
                f"{config['host']}:{config['port']}/{config['database']}",
                connect_args={
                    "charset": config["charset"],
                    "connect_timeout": int(config["timeout"])
                },
                pool_recycle=7200,
                pool_pre_ping=True
            )
            self.Session: Union[Session, Any] = scoped_session(sessionmaker(bind=self.engine))

        except SQLAlchemyError as err:
            logger.error(f"Errore durante la configurazione del database - {err}", exc_info=True)
            raise
        except Exception as err:
            logger.error(f"Errore generico durante la configurazione del database - {err}", exc_info=True)
            raise

    @contextmanager
    def session(self):
        session = self.Session()

        try:
            yield session
            session.commit()

        except (SQLAlchemyError, Exception) as err:
            session.rollback()
            logger.error(f"Errore durante la creazione di una sessione - {err}", exc_info=True)
            raise

        finally:
            session.close()
            self.Session.remove()
            logger.info("Sessione chiusa e rimossa")
