import tensorflow as tf
from .console_logs import train_step_console_log, val_console_log
from .tb_logs import tb_write_scalars


__all__ = ['TrainLogHandler', 'ValLogHandler']


class TrainLogHandler:
    def __init__(self, total_epochs, steps_per_epoch, optimizer, logger):
        self.total_epochs = total_epochs
        self.steps_per_epoch = steps_per_epoch
        self.optimizer = optimizer
        self.logger = logger

    def logging(self, epoch, step, losses, tb_writer):
        self._console_logs(epoch=epoch, step=step, losses=losses)
        self._tb_logs(tb_writer=tb_writer, losses=losses)

    def _console_logs(self, epoch, step, losses):
        log, log_colored = train_step_console_log(
            total_epochs=self.total_epochs,
            steps_per_epoch=self.steps_per_epoch,
            current_epoch=epoch,
            current_step=step,
            losses=losses,
            )
        self.logger.info(log)
        print(log_colored)

    def _tb_logs(self, tb_writer, losses):
        tb_write_scalars(tb_writer, losses, step=self.optimizer.iterations)


class ValLogHandler:
    def __init__(self, total_epochs, logger):
        self.total_epochs = total_epochs
        self.logger = logger

    def logging(self, epoch, losses, tb_writer):
        self._console_logs(epoch=epoch, losses=losses)
        self._tb_logs(tb_writer=tb_writer, epoch=epoch, losses=losses)

    def _console_logs(self, epoch, losses):
        log, log_colored = val_console_log(
            total_epochs=self.total_epochs,
            current_epoch=epoch,
            losses=losses,
            )
        self.logger.info(log)
        print(log_colored)

    def _tb_logs(self, tb_writer, epoch, losses):
        tb_write_scalars(tb_writer, losses, step=epoch)
    