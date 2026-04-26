import streamlit as st
import time
from game import Game
from AI import AI
from config import PLAYER_X, PLAYER_O, BOARD_SIZE

# ========================
# CẤU HÌNH TRANG
# ========================
st.set_page_config(
    page_title="Caro AI",
    page_icon="🎯",
    layout="centered"
)

# ========================
# KHỞI TẠO SESSION STATE
# ========================
if "game" not in st.session_state:
    st.session_state.game = Game()

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Medium"

if "ai" not in st.session_state:
    st.session_state.ai = AI(depth=3)

if "status" not in st.session_state:
    st.session_state.status = "LƯỢT CỦA BẠN (X)"

if "stats" not in st.session_state:
    st.session_state.stats = "AI Stats | Nodes: 0 | Pruned: 0 | Time: 0.00s"

game = st.session_state.game


# ========================
# HÀM RESET GAME
# ========================
def reset_game():
    game.reset()

    difficulty = st.session_state.difficulty

    if difficulty == "Easy":
        depth = 2
    elif difficulty == "Hard":
        depth = 4
    else:
        depth = 3

    st.session_state.ai = AI(depth=depth)
    st.session_state.status = f"{difficulty} | LƯỢT CỦA BẠN (X)"
    st.session_state.stats = "AI Stats | Nodes: 0 | Pruned: 0 | Time: 0.00s"


# ========================
# HÀM AI ĐÁNH
# ========================
def ai_move():
    if game.game_over:
        return

    start_time = time.time()

    move = st.session_state.ai.get_best_move(game.board)

    elapsed = time.time() - start_time

    st.session_state.stats = (
        f"AI Stats | Nodes: {st.session_state.ai.nodes_visited} | "
        f"Pruned: {st.session_state.ai.pruned_branches} | "
        f"Time: {elapsed:.2f}s"
    )

    if move:
        game.make_move(move[0], move[1], PLAYER_O)

    if game.game_over:
        if game.winner == PLAYER_O:
            st.session_state.status = "AI THẮNG!"
        elif game.winner == PLAYER_X:
            st.session_state.status = "BẠN THẮNG!"
        else:
            st.session_state.status = "HÒA!"
    else:
        st.session_state.status = (
            f"{st.session_state.difficulty} | LƯỢT CỦA BẠN (X)"
        )


# ========================
# HEADER
# ========================
st.markdown("# 🎯 CARO AI")

col1, col2, col3 = st.columns([2, 2, 4])

with col1:
    if st.button("NEW GAME"):
        reset_game()
        st.rerun()

with col2:
    selected = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"],
        index=["Easy", "Medium", "Hard"].index(
            st.session_state.difficulty
        )
    )

    if selected != st.session_state.difficulty:
        st.session_state.difficulty = selected
        reset_game()
        st.rerun()

with col3:
    st.info(st.session_state.status)

st.success(st.session_state.stats)

st.divider()


# ========================
# VẼ BÀN CỜ
# ========================
for i in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)

    for j in range(BOARD_SIZE):
        cell = game.board[i][j]

        if cell == PLAYER_X:
            text = "❌"
        elif cell == PLAYER_O:
            text = "⭕"
        else:
            text = " "

        if cols[j].button(text, key=f"{i}-{j}"):

            if game.game_over:
                st.warning("Game đã kết thúc!")
                st.stop()

            if game.current_player != PLAYER_X:
                st.stop()

            if game.board[i][j] != 0:
                st.stop()

            # Người chơi đánh
            game.make_move(i, j, PLAYER_X)

            if game.game_over:
                st.session_state.status = "BẠN THẮNG!"
                st.rerun()

            # AI đánh
            st.session_state.status = "AI ĐANG SUY NGHĨ..."
            ai_move()
            st.rerun()


# ========================
# FOOTER
# ========================
st.divider()
st.caption("Caro AI Project | Python + Minimax + Alpha-Beta Pruning")