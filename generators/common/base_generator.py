"""
Abstract generator.
"""

from abc import ABC, abstractmethod

from generators.common.publish import Publisher


class BaseGenerator(ABC):

    dataset_name = None

    def __init__(self, context):

        self.context = context

    @abstractmethod
    def generate(self):

        pass

    def run(self):

        dataframe = self.generate()

        Publisher.publish(

            dataframe,

            self.dataset_name

        )

        return dataframe