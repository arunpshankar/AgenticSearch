from src.config.client import initialize_genai_client
from src.llm.gemini_text import generate_content
from src.config.setup import GOOGLE_ICON_PATH
from src.utils.template import TemplateLoader
from src.agents.react import run_react_agent
from src.config.logging import logger
from typing import Optional
from typing import Tuple
from pathlib import Path
from typing import List 
import streamlit as st
import requests
import datetime
import base64
import ast
import os
import re


template_loader = TemplateLoader()