"""
Base CDC Generator

Provides common functionality for all CDC generators.
"""

from datetime import datetime
from uuid import uuid4

import pandas as pd

from generators.common.context import GenerationContext


class BaseCDCGenerator:

    def __init__(
        self,
        context: GenerationContext,
        dataframe_name: str
    ):

        self.context = context

        self.dataframe_name = dataframe_name

    ###############################################################

    def append(
        self,
        row: dict
    ):

        timestamp = datetime.now()

        row.update({

            "event_id": str(uuid4()),

            "batch_id": timestamp.strftime(
                "%Y%m%d%H%M"
            ),

            "source_system": "BANKING_SIMULATOR",

            "event_timestamp": timestamp,

            "change_timestamp": timestamp

        })

        dataframe = getattr(

            self.context,

            self.dataframe_name

        )

        new_row = pd.DataFrame([row])

        if dataframe.empty:

            dataframe = new_row

        else:

            dataframe = pd.concat(

                [

                    dataframe,

                    new_row

                ],

                ignore_index=True

            )

        setattr(

            self.context,

            self.dataframe_name,

            dataframe

        )

    ###############################################################

    def get_dataframe(self):

        return getattr(

            self.context,

            self.dataframe_name

        )

    ###############################################################

    def clear(self):

        setattr(

            self.context,

            self.dataframe_name,

            pd.DataFrame()

        )